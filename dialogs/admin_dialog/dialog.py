from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Cancel, Column, Row
from aiogram_dialog.widgets.input import MessageInput, TextInput

from states.state_groups import adminSG
from dialogs.admin_dialog.getters import (send_static, send_message, save_message, get_database, get_user_id, sub_getter, get_days, \
    clean_channels, get_subs_static, subs_malling_choose, mail_choose)

admin_dialog = Dialog(
    Window(
        Const('Меню админ панели'),
        Column(
            SwitchTo(Const('Управление подпиской'), id='sub_manage', state=adminSG.sub_management),
            Button(Const('Получить статистику'), id='get_static', on_click=send_static),
            SwitchTo(Const('Сделать рассылку'), id='start_malling', state=adminSG.get_mail),
            Button(Const('Получить всю базу данных'), id='get_database', on_click=get_database),
            Button(Const('Получить всех подписчиков'), id='get_all_sub', on_click=get_subs_static),
            Button(Const('Удалить отсутствующих в списке'), id='clean_channels', on_click=clean_channels),
            Cancel(Const('Закрыть админку'), id='close_admin_menu')
        ),
        state=adminSG.main
    ),
    Window(
        Const('Отправьте идентификатор юзера'),
        SwitchTo(Const('Назад'), id='back', state=adminSG.main),
        TextInput(
            id='get_user',
            on_success=get_user_id
        ),
        state=adminSG.sub_management
    ),
    Window(
        Format('Юзер: {id}\nИмя: {name}\nЮзернейм(тэг): {username}\n\nПодписка: {sub_date}\n\n'),
        Const('Вы можете добавить к подписке юзера нужное кол-во дней', when='sub'),
        Const('Данный юзер не имеет никакой подписки, поэтому добавление срока отклонено', when='not_sub'),
        Column(
            SwitchTo(Const('Добавить дней'), id='day_add', state=adminSG.sub_change, when='sub'),
            SwitchTo(Const('На главное меню'), id='to_menu', state=adminSG.main)
        ),
        getter=sub_getter,
        state=adminSG.user_info
    ),
    Window(
        Const('Отправьте количество дней для добавление к подписки юзера'),
        SwitchTo(Const('Отмена'), id='to_menu', state=adminSG.main),
        TextInput(
            id='get_days',
            on_success=get_days,
        ),
        state=adminSG.sub_change
    ),
    Window(
        Const('Выберите на какую аудиторию вы хотели бы сделать рассылку'),
        Column(
            Button(Const('На всех'), id='all_mail_choose', on_click=mail_choose),
            Button(Const('На подписчиков'), id='subs_mail_choose', on_click=mail_choose),
            Button(Const('На людей без подписки'), id='users_mail_choose', on_click=mail_choose),
        ),
        SwitchTo(Const('Назад'), id='back', state=adminSG.main),
        state=adminSG.mail_choose
    ),
    Window(
        Const('Отправьте сообщение для рассылки'),
        MessageInput(
            func=save_message,
            content_types=ContentType.ANY
        ),
        SwitchTo(Const('Назад'), id='back_mail_choose', state=adminSG.mail_choose),
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