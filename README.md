# api_yamdb
api_yamdb

правка для тестов

TO DO: ОФОРМИТЬ ФАЙЛ !!!!


Создайте пользователя
    python manage.py createsuperuser

Для запуска проекта
    python manage.py runserver

Для загрузки тестовых данных в БД
    python manage.py load_csv


Changelog:
    2023-09-27
        Не отменяет пункта оформить файл
        В api_yamdb.settings.py добавлена настройка CSV_DIR - директория с CSV файлами для импорта тестовых данных
        Реализован импорт данных из csv файла
            Для загрузки данных нужо выполнить команду python manage.py load_csv
        Добавлены в админку модели Category, Genre, Title, GenreTitle
