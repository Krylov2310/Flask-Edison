import datetime
import os
import random

from flask import url_for
from markupsafe import Markup
from flask_admin import form
from flask_admin.contrib.sqla import ModelView

file_path = os.path.abspath(os.path.dirname(__name__))
STORAGE = os.path.join(file_path, 'files/static/storage_file')


# Таблица
class StorageView(ModelView):
    column_display_pk = True
    column_labels = {
        'id': 'ID',
        'name': 'Имя файла',
        'path': 'Файл',
        'type': 'Тип файла',
        'create_date': 'Дата добавления'
    }

    # Модальные окна
    create_modal = True
    edit_modal = True

    # Обработка файлов
    def _list_thumbnail(StorageView, context, model, name):
        if not model.path:  # path - расширение файлов
            return ''

        url = url_for('static', filename=os.path.join('storage_file/', model.path))  # Создаем URL

        if model.type in ['pdf', 'txt', 'doc', 'html', 'docx', 'xls', 'xslx']:
            return Markup(f'<a href="{url}" target="_blank">Скачать файл</a>')

        if model.type in ['jpg', 'jpeg', 'png', 'svg', 'gif', 'PNG']:
            return Markup(f'<img src="{url}" width="100">')

        if model.type in ['mp3']:
            return Markup(f'<audio controls="controls"><source src="{url}" type="audio/mpeg" /></audio>')

        if model.type in ['mp4', 'MP4', 'avi', 'mpeg']:
            return Markup(
                f'<video width="200" height="150" controls="controls"><source src="{url}" type="audio/mpeg" /></video>')

    # Передаем функцию прямо в строку
    column_formatters = {
        'path': _list_thumbnail
    }

    # Сохраняет файл в папку
    form_extra_fields = {
        "file": form.FileUploadField('',
                                     base_path=STORAGE,
                                     )}

    # Создаем случайное имя
    def _change_path_data(self, _form):
        try:
            storage_file = _form.file.data

            if storage_file is not None:
                hash = random.getrandbits(28)  # Генерирует новое имя
                ext = storage_file.filename.split('.')[-1]  # Определяет расширение файла
                print('ext', ext)
                new_file_name = f'{hash}.{ext}'  # Генерируем новое имя файла
                print('new_file_name', new_file_name)
                create_date = datetime.datetime.now()  # Создаем новую дату

                storage_file.save(
                    os.path.join(STORAGE, new_file_name)
                )  # Сохраняем файл в хранилище

                # Автоматическое заполнение полей
                _form.name.data = _form.name.data or storage_file.filename
                _form.path.data = new_file_name
                _form.type.data = ext
                _form.create_date.data = create_date
                del _form.file
        except Exception as ex:
            pass
        return _form

    # Разрешение на создание формы
    def create_form(self, obj=None):
        return self._change_path_data(
            super(StorageView, self).create_form(obj)
        )

    # Разрешение на редакрирование формы
    def edit_form(self, obj=None):
        return self._change_path_data(
            super(StorageView, self).edit_form(obj)
        )
