from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Cancel, Column, Row
from aiogram_dialog.widgets.input import MessageInput

from states.state_groups import adminSG
from dialogs.admin_dialog.getters import send_static, send_message, save_message, get_database

admin_dialog = Dialog(
    Window(
        Const('Меню админ панели'),
        Column(
            Button(Const('Получить статистику'), id='get_static', on_click=send_static),
            SwitchTo(Const('Сделать рассылку'), id='start_malling', state=adminSG.get_mail),
            Button(Const('Получить всю базу данных'), id='get_database', on_click=get_database),
            Cancel(Const('Закрыть админку'), id='close_admin_menu')
        ),
        state=adminSG.main
    ),
    Window(
        Const('Отправьте сообщение для рассылки'),
        SwitchTo(Const('Назад'), id='back', state=adminSG.main),
        MessageInput(
            func=save_message,
            content_types=ContentType.ANY
        ),
        state=adminSG.get_mail
    ),
    Window(
        Const('Вы подтверждаете рассылку сообщения'),
        Row(
            Button(Const('Да'), id='mallin', on_click=send_message),
            SwitchTo(Const('Нет'), id='back', state=adminSG.main)
        ),
        state=adminSG.malling
    )
)