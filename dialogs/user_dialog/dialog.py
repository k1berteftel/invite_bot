from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import SwitchTo, Start, Button, Column, Row
from aiogram_dialog.widgets.input import TextInput, MessageInput

from states.state_groups import startSG, adminSG
from dialogs.user_dialog.getters import menu, months_save, check_cardpay, check_cryptopay


user_dialog = Dialog(
    Window(
        Const('Приветственное сообщение'),
        Column(
            SwitchTo(Const('Приобрести подписку'), id='subscription', state=startSG.sub_date),
            SwitchTo(Const('О канале'), id='about', state=startSG.about),
            Start(Const('Админ панель'), id='admin', state=adminSG.main, when='admin')
        ),
        getter=menu,
        state=startSG.start
    ),
    Window(
        Const('Выберите срок подписки'),
        Column(
            Button(Const('Месяц'), id='1_month', on_click=months_save),
            Button(Const('6 Месяцев'), id='6_months', on_click=months_save),
            Button(Const('Год'), id='12_months', on_click=months_save),
            SwitchTo(Const('Назад'), id='back', state=startSG.start)
        ),
        state=startSG.sub_date
    ),
    Window(
        Const('Выберите тип оплаты'),
        Column(
            SwitchTo(Const('Карта'), id='card', state=startSG.card),
            SwitchTo(Const('Крипта'), id='crypto', state=startSG.crypto),
            SwitchTo(Const('Назад'), id='back_date', state=startSG.sub_date)
        ),
        state=startSG.subscription
    ),
    Window(
        Const('Реквизиты для оплаты: *****\n После оплаты отправьте фото чека'),
        SwitchTo(Const('Отмена'), id='back_pay', state=startSG.subscription),
        MessageInput(
            func=check_cardpay,
            content_types=ContentType.PHOTO
        ),
        state=startSG.card
    ),
    Window(
        Const('Адрес кошелька для оплаты: **** \nПосле оплаты отправьте хеш транзакции'),
        SwitchTo(Const('Отмена'), id='back_pay', state=startSG.subscription),
        TextInput(
            id='get_cash',
            on_success=check_cryptopay
        ),
        state=startSG.crypto
    ),
    Window(
        Const('Что-то о преимуществах подписки на канал'),
        SwitchTo(Const('Назад'), id='back', state=startSG.start),
        state=startSG.about
    ),
)