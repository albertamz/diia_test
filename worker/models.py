from django.db import models


class RegionalStateAdministration(models.Model):
    edrpou = models.CharField(max_length=65, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    cnap = models.OneToOneField('Cnap', on_delete=models.PROTECT, related_name='address_info')
    locality_name = models.CharField(max_length=255, null=True, blank=True)
    locality_codifier = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255, null=True, blank=True)
    local_community = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    locality = models.CharField(max_length=255, null=True, blank=True)
    village = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    building_number = models.CharField(max_length=100, null=True, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_address(self):
        parts = [self.street, self.building_number]
        if self.city:
            parts.append(self.city)
        elif self.village:
            parts.append(self.village)
        if self.local_community:
            parts.append(self.local_community)
        parts.append(self.region)
        return ', '.join(parts)


class GeneralData(models.Model):
    cnap = models.OneToOneField('Cnap', on_delete=models.PROTECT, related_name='general_info')
    asc_type = models.IntegerField(null=True, blank=True)
    created_by = models.CharField(max_length=255, null=True, blank=True)
    edrpou = models.CharField(max_length=65, null=True, blank=True)
    is_diia = models.BooleanField(null=True, blank=True)
    is_active = models.BooleanField(null=True, blank=True)
    is_inactive = models.BooleanField(null=True, blank=True)
    created_by_type = models.IntegerField(null=True, blank=True)
    is_close_transform = models.BooleanField(null=True, blank=True)
    date_creation_decision_made = models.DateField(null=True, blank=True)
    date_created = models.DateField(null=True, blank=True)
    date_closing_decision_made = models.DateField(null=True, blank=True)
    date_closed = models.DateField(null=True, blank=True)
    is_permanent_working_unit = models.BooleanField(null=True, blank=True)
    is_structural_unit = models.BooleanField(null=True, blank=True)
    consult_phone = models.CharField(max_length=255, null=True, blank=True)
    consult_email = models.CharField(max_length=255, null=True, blank=True)
    num_mobile_center = models.IntegerField(null=True, blank=True)
    has_bus_stop_near = models.BooleanField(null=True, blank=True)
    has_free_parking = models.BooleanField(null=True, blank=True)
    has_free_parking_inv = models.BooleanField(null=True, blank=True)
    has_asc_info_in_city = models.BooleanField(null=True, blank=True)
    num_days_per_week = models.IntegerField(null=True, blank=True)
    num_days_per_week_bef_20 = models.IntegerField(null=True, blank=True)
    has_break = models.BooleanField(null=True, blank=True)
    works_in_saturday = models.BooleanField(null=True, blank=True)
    work_time_mon = models.CharField(max_length=100, null=True, blank=True)
    total_sq = models.FloatField(null=True, blank=True)
    open_reception_sq = models.FloatField(null=True, blank=True)
    open_info_sq = models.FloatField(null=True, blank=True)
    open_waiting_sq = models.FloatField(null=True, blank=True)
    open_service_sq = models.FloatField(null=True, blank=True)
    num_waiting_seats = models.IntegerField(null=True, blank=True)
    num_served_people = models.IntegerField(null=True, blank=True)
    has_otg_contract = models.BooleanField(null=True, blank=True)
    contract_number = models.CharField(max_length=255, null=True, blank=True)
    has_resolution = models.BooleanField(null=True, blank=True)
    resolution_number = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)


class ActivityData(models.Model):
    cnap = models.OneToOneField('Cnap', on_delete=models.PROTECT, related_name='activity_info')
    num_total_empl = models.IntegerField(null=True, blank=True)
    manager_name = models.CharField(max_length=255, null=True, blank=True)
    num_managers = models.IntegerField(null=True, blank=True)
    num_business_reg = models.IntegerField(null=True, blank=True)
    num_realty_reg = models.IntegerField(null=True, blank=True)
    num_residence_reg = models.IntegerField(null=True, blank=True)
    num_other_empl = models.IntegerField(null=True, blank=True)
    num_other_total_empl = models.IntegerField(null=True, blank=True)
    num_other_business_reg = models.IntegerField(null=True, blank=True)
    num_other_realty_reg = models.IntegerField(null=True, blank=True)
    num_other_cadastral_reg = models.IntegerField(null=True, blank=True)
    num_other_residence_reg = models.IntegerField(null=True, blank=True)
    num_other_mia_empl = models.IntegerField(null=True, blank=True)
    num_other_soc_protec_empl = models.IntegerField(null=True, blank=True)
    num_other_other_empl = models.IntegerField(null=True, blank=True)
    has_admin_service_consalt = models.BooleanField(null=True, blank=True)
    has_info_department = models.BooleanField(null=True, blank=True)
    has_phone_consalt = models.BooleanField(null=True, blank=True)
    has_online_consalt = models.BooleanField(null=True, blank=True)
    has_sms_inform = models.BooleanField(null=True, blank=True)
    has_online_inform = models.BooleanField(null=True, blank=True)
    has_phone_inform = models.BooleanField(null=True, blank=True)
    has_chat_bot_inform = models.BooleanField(null=True, blank=True)
    has_personal_inform = models.BooleanField(null=True, blank=True)
    has_mail_inform = models.BooleanField(null=True, blank=True)
    has_other_inform = models.BooleanField(null=True, blank=True)
    has_automatic_queue_handle = models.BooleanField(null=True, blank=True)
    has_prev_appointment_personal = models.BooleanField(null=True, blank=True)
    has_prev_appointment_online = models.BooleanField(null=True, blank=True)
    avg_waiting = models.IntegerField(null=True, blank=True)
    has_free_access_doc_templ = models.BooleanField(null=True, blank=True)
    has_separated_reception_delivery = models.BooleanField(null=True, blank=True)
    has_bank_payment = models.BooleanField(null=True, blank=True)
    has_pos_terminal_payment = models.BooleanField(null=True, blank=True)
    has_self_service_payment = models.BooleanField(null=True, blank=True)
    has_other_payment_system = models.BooleanField(null=True, blank=True)
    has_photocopy = models.BooleanField(null=True, blank=True)
    has_lamination = models.BooleanField(null=True, blank=True)
    has_photograpy = models.BooleanField(null=True, blank=True)
    has_free_wifi = models.BooleanField(null=True, blank=True)
    has_stationery_sale = models.BooleanField(null=True, blank=True)
    has_corner_self_service = models.BooleanField(null=True, blank=True)
    manager_self_esteem = models.CharField(max_length=255, null=True, blank=True)
    num_trained_empl = models.IntegerField(null=True, blank=True)
    has_feedback_box = models.BooleanField(null=True, blank=True)
    has_feedback_book = models.BooleanField(null=True, blank=True)
    has_google_map_feedback = models.BooleanField(null=True, blank=True)
    has_chat_bot_feedback = models.BooleanField(null=True, blank=True)
    other_feedback = models.CharField(max_length=255, null=True, blank=True)
    num_feedback_total = models.IntegerField(null=True, blank=True)
    num_feedback_positive = models.IntegerField(null=True, blank=True)
    num_feedback_negative = models.IntegerField(null=True, blank=True)
    has_technical_room = models.BooleanField(null=True, blank=True)
    has_ramp = models.BooleanField(null=True, blank=True)
    has_stairs_with_handrails = models.BooleanField(null=True, blank=True)
    has_equiped_technical_room = models.BooleanField(null=True, blank=True)
    has_braille_font = models.BooleanField(null=True, blank=True)
    has_deaf_adaptation = models.BooleanField(null=True, blank=True)
    has_temp_place_strollers = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Activity Data for {self.cnap}"


class InfoSupportData(models.Model):
    cnap = models.OneToOneField('Cnap', on_delete=models.PROTECT, related_name='info_support_info')
    has_person_org_register = models.BooleanField(null=True, blank=True)
    has_real_estate_rights_register = models.BooleanField(null=True, blank=True)
    has_demography_register = models.BooleanField(null=True, blank=True)
    has_land_cadastre = models.BooleanField(null=True, blank=True)
    other_registers = models.TextField(null=True, blank=True)
    has_e_sevices = models.BooleanField(null=True, blank=True)
    e_services_name = models.CharField(max_length=255, null=True, blank=True)
    has_edm_system = models.BooleanField(null=True, blank=True)
    edm_system_name = models.CharField(max_length=255, null=True, blank=True)
    edm_system_developer = models.CharField(max_length=255, null=True, blank=True)
    has_website_access = models.BooleanField(null=True, blank=True)
    has_phone_access = models.BooleanField(null=True, blank=True)
    has_info_terminal_access = models.BooleanField(null=True, blank=True)
    has_info_stand_access = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Info Support for {self.cnap}"


class AdminServiceData(models.Model):
    cnap = models.OneToOneField('Cnap', on_delete=models.PROTECT, related_name='admin_service_info')
    num_total_services = models.IntegerField(null=True, blank=True)
    num_e_services = models.IntegerField(null=True, blank=True)
    num_rsa_services = models.IntegerField(null=True, blank=True)
    num_dsa_services = models.IntegerField(null=True, blank=True)
    num_city_services = models.IntegerField(null=True, blank=True)
    num_asc_services = models.IntegerField(null=True, blank=True)
    num_special_services = models.IntegerField(null=True, blank=True)
    is_all_asc_services_via_center = models.BooleanField(null=True, blank=True)
    num_all_asc_e_services = models.IntegerField(null=True, blank=True)
    num_from_this_year_start = models.IntegerField(null=True, blank=True)
    num_services_residence = models.IntegerField(null=True, blank=True)
    num_services_passport = models.IntegerField(null=True, blank=True)
    num_services_vehicle = models.IntegerField(null=True, blank=True)
    num_acts_services = models.IntegerField(null=True, blank=True)
    num_dzk_services = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Admin Services for {self.cnap}"


class Cnap(models.Model):
    idf = models.CharField(max_length=255, primary_key=True, db_index=True)
    name = models.CharField(max_length=510)
    regional_state_administration = models.ForeignKey(
        RegionalStateAdministration, on_delete=models.PROTECT, related_name='cnaps'
    )
    address = models.OneToOneField(
        Address, null=True, blank=True, on_delete=models.PROTECT, related_name='cnap_address'
    )
    general_data = models.OneToOneField(
        GeneralData, on_delete=models.PROTECT, null=True, blank=True, related_name='cnap_general_data'
    )
    activity_data = models.OneToOneField(
        ActivityData, on_delete=models.PROTECT, null=True, blank=True, related_name='cnap_activity_data'
    )
    info_support_data = models.OneToOneField(
        InfoSupportData, on_delete=models.PROTECT, null=True, blank=True, related_name='cnap_info_support_data'
    )
    admin_service_data = models.OneToOneField(
        AdminServiceData, on_delete=models.PROTECT, null=True, blank=True, related_name='cnap_admin_service_data'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


class ResponsePerson(models.Model):
    cnap = models.ForeignKey(Cnap, on_delete=models.CASCADE, related_name='response_persons')
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255,null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    ceo_contact_pip = models.CharField(max_length=255, null=True, blank=True)
    ceo_contact_phone = models.CharField(max_length=255, null=True, blank=True)
    ceo_contact_mail = models.EmailField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
