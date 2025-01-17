import datetime
import os
import random
import cv2
import numpy as np

from flask import url_for
from markupsafe import Markup
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
# from models import Dashboard

file_path = os.path.abspath(os.path.dirname(__name__))
STORAGE = os.path.join(file_path, 'files/static/media_file')

# Словари для поиска объектов
VOC_LABELS = [
    "background", "aeroplane", "bicycle", "bird", "boat", "bottle",
    "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant",
    "sheep", "sofa", "train", "tvmonitor"]


# Таблица
class DasboardView(ModelView):
    column_display_pk = True
    column_labels = {
        'id': 'ID',
        'name': 'Имя файла',
        'image': 'Путь файла',
        'processed_image': 'Распознанный файл',
        'type': 'Формат файла',
        'object_type': 'Координаты',
        'confidence': 'Класс распознавания',
        'location': 'location',
        'create_date': 'Дата'
    }

    # исключенные колонки
    # column_exclude_list = ['id', 'object_type', 'confidence', 'location']
    # Модальные окна
    can_create = True  # Разрешение на создание
    can_edit = True  # Разрешение на редактирование
    can_delete = True  # Разрешение на удаление

    # Обработка файлов
    def _list_thumbnail(DasboardView, context, model, name):
        if not model.image:  # path - расширение файлов
            print('model.path', model.image)
            return ''

        url = url_for('static', filename=os.path.join('media_file/', model.image))  # Создаем URL

        # Проверяем формат файла
        if model.type in ['jpg', 'jpeg', 'png', 'svg', 'gif', 'PNG']:
            return Markup(f'<img src="{url}" width="100">')

    # Передаем функцию прямо в строку
    column_formatters = {'image': _list_thumbnail}

    # Сохраняет файл в папку
    form_extra_fields = {"file": form.FileUploadField('', base_path=STORAGE, )}

    # Создаем случайное имя
    def _change_path_data(self, _form):
        print('_form', _form)
        try:
            storage_file = _form.file.data

            if storage_file is not None:
                hash = random.getrandbits(128)  # Генерирует новое имя
                ext = storage_file.filename.split('.')[-1]  # Определяет расширение файла
                print('ext', ext)
                new_file_name = f'{hash}.{ext}'  # Собираем новое имя файла
                print('new_file_name', new_file_name)
                create_date = datetime.datetime.now()  # Создаем новую дату
                print('create_date', create_date)

                storage_file.save(
                    os.path.join(STORAGE, new_file_name)
                )  # Сохраняем файл в хранилище

                # Автоматическое заполнение полей
                _form.name.data = _form.name.data or storage_file.filename
                _form.image.data = new_file_name
                _form.type.data = ext
                _form.create_date.data = create_date
                del _form.file
        except Exception as ex:
            pass
        return _form

    # Разрешение на создание формы
    def create_form(self, obj=None):
        return self._change_path_data(
            super(DasboardView, self).create_form(obj)
        )

    # Разрешение на редакрирование формы
    def edit_form(self, obj=None):
        return self._change_path_data(
            super(DasboardView, self).edit_form(obj)
        )
