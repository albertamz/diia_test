import requests
from constance import config
from datetime import datetime
from celery.schedules import crontab

from cnap_monitoring.celery import app as celery_app
from worker.decorators import benchmark
from worker.models import (RegionalStateAdministration, Cnap, Address, GeneralData, ActivityData, InfoSupportData,
                           AdminServiceData, ResponsePerson)

import logging
logger = logging.getLogger('worker')


@celery_app.task
@benchmark
def parse_data(year: int, quarter: int):
    logger.info(f'Parsing data for year {year} and quarter {quarter} started')
    static_reports_url = f'{config.STATIC_REPORT_LIST_URL}/{year}/{quarter}/?format=json'

    try:
        response = requests.get(static_reports_url)
        response.raise_for_status()
        data = response.json().get('results', [])
    except requests.RequestException as e:
        logger.error(f"Failed to fetch report list: {e}")
        return
    logger.info(f'Fetched reports for year: {year} / quarter: {quarter}')

    for item in data:
        edrpou = item['rsa']['edrpou']
        report_id = item['id']
        rsa, created = RegionalStateAdministration.objects.get_or_create(
            edrpou=edrpou,
            defaults={'name': item['rsa']['name'], 'address': item['rsa']['address']}
        )
        if not created:
            if rsa.name != item['rsa']['name'] or rsa.address != item['rsa']['address']:
                rsa.name = item['rsa']['name']
                rsa.address = item['rsa']['address']
                rsa.save()

        logger.info(f'Processing report ID {report_id}')
        list_of_ids = []
        page_num = 1

        while True:
            static_reports_entries_url = f'{config.STATIC_REPORT_ENTRIES_URL}/{report_id}?format=json&page={page_num}'
            try:
                response = requests.get(static_reports_entries_url)
                response.raise_for_status()
                detail_data = response.json()
                list_of_ids.extend(item['id'] for item in detail_data.get('results', []))
            except requests.RequestException as e:
                logger.error(f"Failed to fetch details for report ID {report_id} on page {page_num}: {e}")
                break

            if not detail_data.get('next'):
                break
            page_num += 1

        logger.info(f'Fetched {len(list_of_ids)} IDFs for report ID {report_id}')

        for id in list_of_ids:
            static_reports_detail_url = f'{config.STATIC_REPORT_DETAIL_URL}/{id}?format=json'
            try:
                response = requests.get(static_reports_detail_url)
                response.raise_for_status()
                data = response.json()['results'][0]
            except requests.RequestException as e:
                logger.error(f"Failed to fetch details for IDF {id}: {e}")
                continue
            logger.info(f'Processing IDF {id}')
            cnap, _ = Cnap.objects.get_or_create(idf=data['asc_org']['idf'], regional_state_administration=rsa)

            if cnap.name != data['asc_org']['name']:
                cnap.name = data['asc_org']['name']

            address, _ = Address.objects.get_or_create(
                cnap=cnap
            )
            address.locality_name = data['asc_org']['address']['locality']['name'] if \
                data['asc_org']['address']['locality'] else None
            address.locality_codifier = data['asc_org']['address']['locality']['codifier'] if \
            data['asc_org']['address']['locality'] else None
            address.postal_code = data['asc_org']['address']['postal_code']
            address.region = data['general_data']['region']
            address.district = data['general_data']['district']
            address.local_community = data['general_data']['local_community']
            address.city = data['general_data']['city']
            address.locality = data['general_data']['locality']
            address.village = data['general_data']['village']
            address.street = data['general_data']['street']
            address.building_number = data['general_data']['building_number']
            address.latitude = data['asc_org']['address']['lat']
            address.longitude = data['asc_org']['address']['lon']
            address.save()
            cnap.address = address

            general_data, _ = GeneralData.objects.get_or_create(
                cnap=cnap
            )
            fields = ['asc_type', 'created_by', 'edrpou', 'is_diia', 'is_active', 'is_inactive', 'created_by_type',
                      'is_close_transform', 'date_creation_decision_made', 'date_created', 'date_closing_decision_made',
                      'date_closed', 'is_permanent_working_unit', 'is_structural_unit', 'consult_phone',
                      'consult_email', 'num_mobile_center', 'has_bus_stop_near', 'has_free_parking',
                      'has_free_parking_inv', 'has_asc_info_in_city', 'num_days_per_week', 'num_days_per_week_bef_20',
                      'has_break', 'works_in_saturday', 'work_time_mon', 'total_sq', 'open_reception_sq',
                      'open_info_sq', 'open_waiting_sq', 'open_service_sq', 'num_waiting_seats', 'num_served_people',
                      'has_otg_contract', 'contract_number', 'has_resolution', 'resolution_number', 'website']
            for field in fields:
                setattr(general_data, field, data['general_data'][field])
            general_data.save()
            cnap.general_data = general_data

            activity_data, _ = ActivityData.objects.get_or_create(
                cnap=cnap
            )
            fields = ['num_total_empl', 'manager_name', 'num_managers', 'num_business_reg', 'num_realty_reg',
                      'num_residence_reg', 'num_other_empl', 'num_other_total_empl', 'num_other_business_reg',
                      'num_other_realty_reg', 'num_other_cadastral_reg', 'num_other_residence_reg',
                      'num_other_mia_empl', 'num_other_soc_protec_empl', 'num_other_other_empl',
                      'has_admin_service_consalt', 'has_info_department', 'has_phone_consalt', 'has_online_consalt',
                      'has_sms_inform', 'has_online_inform', 'has_phone_inform', 'has_chat_bot_inform',
                      'has_personal_inform', 'has_mail_inform', 'has_other_inform', 'has_automatic_queue_handle',
                      'has_prev_appointment_personal', 'has_prev_appointment_online', 'avg_waiting',
                      'has_free_access_doc_templ', 'has_separated_reception_delivery', 'has_bank_payment',
                      'has_pos_terminal_payment', 'has_self_service_payment', 'has_other_payment_system',
                      'has_photocopy', 'has_lamination', 'has_photograpy', 'has_free_wifi', 'has_stationery_sale',
                      'has_corner_self_service', 'manager_self_esteem', 'num_trained_empl', 'has_feedback_box',
                      'has_feedback_book', 'has_google_map_feedback', 'has_chat_bot_feedback', 'other_feedback',
                      'num_feedback_total', 'num_feedback_positive', 'num_feedback_negative', 'has_technical_room',
                      'has_ramp', 'has_stairs_with_handrails', 'has_equiped_technical_room', 'has_braille_font',
                      'has_deaf_adaptation', 'has_temp_place_strollers']
            for field in fields:
                setattr(activity_data, field, data['activity_data'][field])
            activity_data.save()
            cnap.activity_data = activity_data

            info_support_data, _ = InfoSupportData.objects.get_or_create(
                cnap=cnap
            )
            fields = ['has_person_org_register', 'has_real_estate_rights_register', 'has_demography_register',
                      'has_land_cadastre', 'other_registers', 'has_e_sevices', 'e_services_name', 'has_edm_system',
                      'edm_system_name', 'edm_system_developer', 'has_website_access', 'has_phone_access',
                      'has_info_terminal_access', 'has_info_stand_access']
            for field in fields:
                setattr(info_support_data, field, data['info_support_data'][field])
            info_support_data.save()
            cnap.info_support_data = info_support_data

            admin_service_data, _ = AdminServiceData.objects.get_or_create(
                cnap=cnap
            )
            fields = ['num_total_services', 'num_e_services', 'num_rsa_services', 'num_dsa_services',
                      'num_city_services', 'num_asc_services', 'num_special_services', 'is_all_asc_services_via_center',
                      'num_all_asc_e_services', 'num_from_this_year_start', 'num_services_residence',
                      'num_services_passport', 'num_services_vehicle', 'num_acts_services', 'num_dzk_services']
            for field in fields:
                setattr(admin_service_data, field, data['admin_service_data'][field])
            admin_service_data.save()
            cnap.admin_service_data = admin_service_data

            response_person, _ = ResponsePerson.objects.get_or_create(
                cnap=cnap
            )
            fields = ['name', 'phone', 'email', 'ceo_contact_pip', 'ceo_contact_phone', 'ceo_contact_mail']
            for field in fields:
                setattr(response_person, field, data['resp_person_data'][field])
            response_person.save()
            cnap.response_person = response_person
            cnap.save()
            logger.info(f'Processing ID {id} finished')
        logger.info(f'Processing report ID {report_id} finished')
    logger.info(f'Parsing data for year {year} and quarter {quarter} finished')

@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=3, minute=0, day_of_month="1", month_of_year="1,4,7,10"),
        parse_data_with_dynamic_args.s()
    )

def get_previous_year_and_quarter():
    now = datetime.now()
    quarter = (now.month - 1) // 3 + 1

    if quarter == 1:
        previous_year = now.year - 1
        previous_quarter = 4
    else:
        previous_year = now.year
        previous_quarter = quarter - 1

    return previous_year, previous_quarter

@celery_app.task
def parse_data_with_dynamic_args():
    year, quarter = get_previous_year_and_quarter()
    parse_data.delay(year=year, quarter=quarter)
