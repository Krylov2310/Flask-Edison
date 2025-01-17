import datetime
import os
import random
import cv2
import numpy as np

from flask import url_for
from markupsafe import Markup
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from models import ImageFeed


file_path = os.path.abspath(os.path.dirname(__name__))
STORAGE = os.path.join(file_path, 'files/static/media_file')


# Таблица
class ImageFeedView(ModelView):
    column_display_pk = True
    column_labels = {
        'id': 'ID',
        'name': 'Имя файла',
        'image': 'Ваша картинка',
        'processed_image': 'Распознанный файл',
        'type': 'Формат файла',
        'create_date': 'Дата'
    }

    # исключенные колонки
    column_exclude_list = ['id', 'type']
    # Модальные окна
    can_create = True  # Разрешение на создание
    can_edit = False  # Разрешение на редактирование
    can_delete = False  # Разрешение на удаление

    # Обработка файлов
    def _list_thumbnail(ImageFeedView, context, model, name):
        if not model.image:  # path - расширение файлов
            print('model.path', model.image)
            return ''

        url = url_for('static', filename=os.path.join('media_file/', model.image))  # Создаем URL
        # url2 = url_for('static', filename=os.path.join('media_file/', model.processed_image))  # Создаем URL

        # Проверяем формат файла
        if model.type in ['jpg', 'jpeg', 'png', 'svg', 'gif', 'PNG']:
            return Markup(f'<img src="{url}" width="100">')

        #     # Проверяем формат файла
        # if model.type in ['jpg', 'jpeg', 'png', 'svg', 'gif', 'PNG']:
        #     return Markup(f'<img src="{url2}" width="100">')


    # Передаем функцию прямо в строку
    column_formatters = {'image': _list_thumbnail}

    # Сохраняет файл в папку
    form_extra_fields = {"file": form.FileUploadField('', base_path=STORAGE, )}

    # Создаем случайное имя
    def _change_path_data(self, _form):
        try:
            storage_file = _form.file.data

            if storage_file is not None:
                hash = random.getrandbits(128)  # Генерирует новое имя
                ext = storage_file.filename.split('.')[-1]  # Определяет расширение файла
                new_file_name = f'{hash}.{ext}'  # Собираем новое имя файла
                create_date = datetime.datetime.now()  # Создаем новую дату

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
            super(ImageFeedView, self).create_form(obj)
        )

    # Разрешение на редакрирование формы
    def edit_form(self, obj=None):
        return self._change_path_data(
            super(ImageFeedView, self).edit_form(obj)
        )
