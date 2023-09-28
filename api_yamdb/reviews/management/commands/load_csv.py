"""Загрузка тестовых данных в БД для тестирования
Сделано по мотивам статьи
    https://stacktuts.com/how-to-import-csv-data-into-django-models

Для запуска выполнить python manage.py load_csv
"""

import csv

from api_yamdb.settings import CSV_DIR
from django.core.management import BaseCommand, call_command
from django.db import IntegrityError

from reviews.models import Category, Genre, Title

MODELS_FILES = {
    Category: "category.csv",
    Genre: "genre.csv",
    Title: "titles.csv",
    Title.genre.through: "genre_title.csv",
}

FOREIGN_KEY_LIST = [
    "author",
    "category",
]


def clear(self, *args, **kwargs):
    """Функция очистки базы данных."""
    call_command("flush", verbosity=0, interactive=False)
    self.stdout.write(self.style.SUCCESS("База данных успешно очищена."))


def load_csv(self):
    for model, file in MODELS_FILES.items():
        success = f"Таблица {model.__qualname__} успешно загружена."
        error_load = f"Не удалось загрузить таблицу {model.__qualname__}."
        file_path = f"{CSV_DIR}/{file}"

        try:
            with open(file_path, "r", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)
                for data in reader:
                    updated_data = {}
                    for key, value in data.items():
                        if key in FOREIGN_KEY_LIST:
                            updated_data[f"{key}_id"] = value
                        else:
                            updated_data[key] = value
                    model.objects.create(**updated_data)
                self.stdout.write(self.style.SUCCESS(success))

        except (ValueError, IntegrityError, FileNotFoundError) as error:
            self.stdout.write(
                self.style.ERROR(f"Ошибка в загрузке. {error}. {error_load}")
            )


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        clear(self)
        load_csv(self)
