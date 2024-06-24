from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import SwitchTo, Start, Button, Column, Url
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.media import DynamicMedia

from dialogs.user_dialog.getters import menu, about, months_save, check_cardpay, check_cryptopay, sub_getter, crypto_getter, card_getter
from states.state_groups import startSG, adminSG

user_dialog = Dialog(
    Window(
        DynamicMedia('photo'),
        Format('{text}'),
        Column(
            SwitchTo(Const('💵 Оплатить доступ'), id='subscription', state=startSG.sub_date),
            SwitchTo(Const('🔎 Подробнее о клубе'), id='about', state=startSG.about),
            Url(Const('👩‍💻Задать вопрос'), id='question', url=Const('https://t.me/gambIer_kurt')),
            SwitchTo(Const('Профиль'), id='profile', state=startSG.profile),
            Start(Const('Админ панель'), id='admin', state=adminSG.main, when='admin')
        ),
        getter=menu,
        state=startSG.start
    ),
    Window(
        Format(
            '<b>Пользователь</b>: {id}\n\nПодписка: {sub}\n\nДля приобретения или продления подписки выберите пункт «оплатить доступ»'),
        Column(
            SwitchTo(Const('💵 Оплатить доступ'), id='to_sub', state=startSG.sub_date),
            SwitchTo(Const('🔙 Назад'), id='back', state=startSG.start),
        ),
        getter=sub_getter,
        state=startSG.profile
    ),
    Window(
        Const('Выберите срок подписки'),
        Column(
            Button(Const('🐗 2 месяца'), id='2_month', on_click=months_save),
            Button(Const('🐘 6 месяцев'), id='6_months', on_click=months_save),
            Button(Const('🦏 12 месяцев'), id='12_months', on_click=months_save),
            SwitchTo(Const('🔙Назад'), id='back', state=startSG.start)
        ),
        state=startSG.sub_date
    ),
    Window(
        Const('Выберите удобный вид оплаты:'),
        Column(
            SwitchTo(Const('💳 Картой (любая волюта)'), id='card', state=startSG.card),
            SwitchTo(Const('⚡️ USDT (trc-20)'), id='crypto', state=startSG.crypto),
            Url(Const('👩‍💻 Задать вопрос'), id='question', url=Const('https://t.me/gambIer_kurt')),
            SwitchTo(Const('🔙 Назад'), id='back_date', state=startSG.sub_date)
        ),
        state=startSG.subscription
    ),
    Window(
        Format('Вы выбрали: {months} за {price} USD. 🎉\n\n'
               'Для получения реквизитов для оплаты необходимо написать на мой второй аккаунт (@gambIer_kurt) 🏆'
               '\n\nПосле оплаты нажмите «Я оплатил» 👇'),
        Column(
            SwitchTo(Const('✅ Я оплатил'), id='confirm_pay', state=startSG.confirm_card),
            SwitchTo(Const('🔙 Назад'), id='back_pay', state=startSG.subscription),
        ),
        getter=card_getter,
        state=startSG.card
    ),
    Window(
        Const('<b>Отправьте, пожалуйста, Transaction ID (хэш)</b>'),
        SwitchTo(Const('🔙 Назад'), id='back_pay', state=startSG.subscription),
        TextInput(
            id='get_cash_card',
            on_success=check_cardpay
        ),
        state=startSG.confirm_card
    ),
    Window(
        Format('Отправьте\n{price} USDT в сети TRC-20\nНа адрес:\n<code>TLhS4daX8Yj21PGYDAEgsvjz21q5gwCVff</code>\n'
               '\n<em>*кликните на номер счета и он скопируется</em>\nПосле оплаты нажмите Я оплатил 👇'),
        Column(
            SwitchTo(Const('✅ Я оплатил'), id='confirm_pay', state=startSG.confirm_crypto),
            SwitchTo(Const('🔙 Назад'), id='back_pay', state=startSG.subscription),
        ),
        getter=crypto_getter,
        state=startSG.crypto
    ),
    Window(
        Const('<b>Отправьте, пожалуйста, Transaction ID (хэш)</b>'),
        SwitchTo(Const('🔙 Назад'), id='back_pay', state=startSG.subscription),
        TextInput(
            id='get_cash_card',
            on_success=check_cryptopay
        ),
        state=startSG.confirm_crypto
    ),
    Window(
        Format('{text}'),
        Column(
            SwitchTo(Const('🔙 Назад'), id='back', state=startSG.start)
        ),
        getter=about,
        state=startSG.about
    ),
)
