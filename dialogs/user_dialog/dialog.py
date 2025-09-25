from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import SwitchTo, Start, Button, Column, Url
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.media import DynamicMedia

from dialogs.user_dialog.getters import menu, about, months_save, check_cardpay, check_cryptopay, sub_getter, crypto_getter, card_getter, \
    crypto_choose
from states.state_groups import startSG, adminSG

user_dialog = Dialog(
    Window(
        DynamicMedia('photo'),
        Format('{text}'),
        Column(
            SwitchTo(Const('ВСТУПИТЬ В КЛУБ ←'), id='subscription', state=startSG.sub_date),
            SwitchTo(Const('ВНУТРЯНКА КЛУБА'), id='about', state=startSG.about),
            Url(Const('ПОДДЕРЖКА 👩‍💻'), id='question', url=Const('https://t.me/gambIer_kurt')),
            SwitchTo(Const('МОЙ ПРОФИЛЬ'), id='profile', state=startSG.profile),
            Start(Const('Админ панель'), id='admin', state=adminSG.main, when='admin')
        ),
        getter=menu,
        state=startSG.start
    ),
    Window(
        Format(
            '<b>Имя пользователя:</b> {name}\n<b>Юзернейм пользователя:</b> {username}\n'
            '<b>Айди пользователя</b>: {id}\n\nПодписка: {sub}\n\nДля приобретения или продления подписки выберите пункт '
            '<b>«оплатить доступ»</b>👇👇👇'),
        Column(
            SwitchTo(Const('ОПЛАТИТЬ ДОСТУП ←'), id='to_sub', state=startSG.sub_date),
            SwitchTo(Const('НАЗАД'), id='back', state=startSG.start),
        ),
        getter=sub_getter,
        state=startSG.profile
    ),
    Window(
        Const('<b>Тариф:</b> Закрытый клуб Курта 👊\n<b>Стоимость:</b> 89$\n<b>Срок действия:</b> 2 месяца\n\n'
              '<b>Вы получаете доступ к следующим ресурсам:</b>\n• [ПРИВАТ] БОЙЦОВСКИЙ КУРТ\n• [ПРИВАТ] Быстрые схемы'
              '\n• [ПРИВАТ] Инвестиции\n• [ПРИВАТ] Новости\n• [ПРИВАТ] Саморазвитие\n\n• [ПРИВАТ ЧАТ БК] Основа\n'
              '• [ПРИВАТ ЧАТ БК] Флудильня'),
        Column(
            Button(Const('ОПЛАТИТЬ ДОСТУП ←'), id='2_month', on_click=months_save),
            SwitchTo(Const('НАЗАД'), id='back', state=startSG.start)
        ),
        state=startSG.sub_date
    ),
    Window(
        Const('Выберите удобный вид оплаты:'),
        Column(
            SwitchTo(Const('ОПЛАТА В USDT ←'), id='crypto', state=startSG.crypto_choose),
            SwitchTo(Const('ОПЛАТА КАРТОЙ РФ'), id='card', state=startSG.card),
            Url(Const('ПОДДЕРЖКА 👩‍💻'), id='question', url=Const('https://t.me/gambIer_kurt')),
            SwitchTo(Const('НАЗАД'), id='back_date', state=startSG.sub_date)
        ),
        state=startSG.subscription
    ),
    Window(
        Const('Выберите подходящий для вас вариант перевода:'),
        Column(
            Button(Const('USDT в сети TRC20'), id='TRC20', on_click=crypto_choose),
            Button(Const('USDT в сети BEP20'), id='BEP20', on_click=crypto_choose),
            Button(Const('USDT в сети APTOS'), id='APTOS', on_click=crypto_choose),
        ),
        SwitchTo(Const('НАЗАД'), id='back_pay', state=startSG.subscription),
        state=startSG.crypto_choose
    ),
    Window(
        Format('Вы выбрали: {months} за {price} USD. 🎉\n\n'
               'Для получения реквизитов для оплаты необходимо написать на мой второй аккаунт (@gambIer_kurt) 🏆'
               '\n\nПосле оплаты нажмите <b>«Я оплатил»</b> 👇'),
        Column(
            SwitchTo(Const('✅ Я оплатил'), id='confirm_pay', state=startSG.confirm_card),
            SwitchTo(Const('НАЗАД'), id='back_pay', state=startSG.subscription),
        ),
        getter=card_getter,
        state=startSG.card
    ),
    Window(
        Const('<b>Отправьте, пожалуйста, Transaction ID (хэш)</b>'),
        SwitchTo(Const('НАЗАД'), id='back_pay', state=startSG.subscription),
        TextInput(
            id='get_cash_card',
            on_success=check_cardpay
        ),
        state=startSG.confirm_card
    ),
    Window(
        Format('Отправьте <b>{price} USDT</b> в сети <b>{lan}</b>\n\nНа адрес:\n <code>{link}</code>\n'
               '\n<em>*кликните на номер счета и он скопируется</em>\n\nПосле оплаты нажмите <b>«Я оплатил»</b> 👇'),
        Column(
            SwitchTo(Const('✅ Я оплатил'), id='confirm_pay', state=startSG.confirm_crypto),
            SwitchTo(Const('НАЗАД'), id='back_pay', state=startSG.subscription),
        ),
        getter=crypto_getter,
        state=startSG.crypto
    ),
    Window(
        Const('<b>Отправьте, пожалуйста, Transaction ID (хэш)</b>'),
        SwitchTo(Const('НАЗАД'), id='back_pay', state=startSG.subscription),
        TextInput(
            id='get_cash_card',
            on_success=check_cryptopay
        ),
        state=startSG.confirm_crypto
    ),
    Window(
        Format('{text}'),
        Column(
            SwitchTo(Const('ОПЛАТИТЬ ДОСТУП ←'), id='to_sub', state=startSG.sub_date),
            SwitchTo(Const('НАЗАД'), id='back', state=startSG.start)
        ),
        getter=about,
        state=startSG.about
    ),
)
