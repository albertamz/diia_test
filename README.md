# diia_test
## Для запуску проєкта необхідно встоновити на пк:
```
1. Python 3
2. Docker
3. Docker-compose
```

## Інструкція по запуску проєкта:
```
1. Склонувати репозиторій на свій пк
2. Перейти в папку проєкта
3. Створити файл .env за прикладом .env.example
3. Виконати команду docker-compose build
4. Виконати команду docker-compose up
```
# Для ручного запуску скріпта:
```
1. docker container exec -it diia_django_app bash
2. python manage.py shell
3. from worker.tasks import parse_data
4. parse_data()
5. Логи можна переглянути в файлах logs/worker.log та logs/benchmark.log
```
