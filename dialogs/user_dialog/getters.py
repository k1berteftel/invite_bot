from aiogram import Bot
from aiogram.types import Message, CallbackQuery, User, InlineKeyboardButton, InlineKeyboardMarkup, ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from states.state_groups import startSG
from config_data.config import Config, load_config
from database.action_data_class import DataInteraction

config: Config = load_config()


async def card_getter(dialog_manager: DialogManager, **kwargs):
    months = dialog_manager.dialog_data.get('months')
    print(months)
    if months == 2:
        price = 79
        months = '2 месяца'
    elif months == 6:
        price = 229
        months = '6 месяцев'
    else:
        months = '12 месяцев'
        price = 429
    dialog_manager.dialog_data['price'] = price
    return {
        'months': months,
        'price': price
    }


async def crypto_getter(dialog_manager: DialogManager, **kwargs):
    months = dialog_manager.dialog_data.get('months')
    print(months)
    if months == 2:
        price = 79
        dialog_manager.dialog_data['price'] = price
    elif months == 6:
        price = 229
    else:
        price = 429
    dialog_manager.dialog_data['price'] = price
    return {'price': price}


async def sub_getter(session: DataInteraction, event_from_user: User, **kwargs):
    sub = await session.get_sub_date(event_from_user.id)
    if sub:
        is_sub = f'✅Присутствует\n<b>Дата окончания подписки</b>: {sub}\n'
    else:
        is_sub = '❌Отсутствует'
    return {
        'id': event_from_user.id,
        'sub': is_sub
    }


async def menu(event_from_user: User, **kwargs):
    admin = False
    if event_from_user.id in config.bot.admin_ids:
        admin = True
    image_id = "AgACAgIAAxkBAAIBw2Z3BDt2vUYgAfpH2UnNzBZ76xkfAAK33jEbWRa4Sx87TPnSUD6jAQADAgADeQADNQQ"  # Your file_id
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
    text = '<b>Закрытый Клуб по Заработку Бойцовский Курт</b> 💀\n\n' \
           '<em>Клуб создан для людей, которые хотят изменить свою жизнь!</em>\n\n' \
           'Здесь онлайн формат. Бабки из любой точки мира.\nЗдесь развиваются как физически, так и ментально.\n\n' \
           '<em>Это место станет твоей отправной точкой в новую жизнь!</em> 🏆\n\n' \
           '<b>ЕСЛИ ТЕБЯ ЭТО ВДОХНОВЛЯЕТ, ТО ТЫ ГОТОВ.</b>\n<b>ЕСЛИ ЭТО НЕ ПРО ТЕБЯ — ПРОЙДИ МИМО.</b>\n\n' \
           'ГАРАНТИЯ УСПЕХА — ТВОЯ ЛИЧНАЯ ОТВЕТСТВЕННОСТЬ'
    return {'admin': admin,
            'text': text,
            'photo': image}

async def about(**kwargs):
    text = '<b>НАХОДЯСЬ В КЛУБЕ ТЫ ПОЛУЧИШЬ👇</b>\n\n<b>✅ МАНИМЕЙКИНГ </b>\n\n' \
           'Зарабатывать деньги-навык, которому может обучиться \nкаждый, достаточно лишь знать алгоритм работы. \n' \
           '<b>И Я ДАМ ТЕБЕ ЕГО.</b>\n\n<b>✅ КОМАНДА</b>\n\nНа твоем пути открываются <b>ВОЗМОЖНОСТИ</b>. ' \
           'Ты пробуждаешься. Больше не нужно быть подстилкой для общества и стыдиться своих амбиций.\n\n ' \
           '<b>✅ ГАЙДЫ И ПОСТЫ</b>\n\nВ них затронуты все направления для твоего развития, начиная ' \
           'от мышления, мотивации, изменения образа жизни до финансов. <b>МАКСИМАЛЬНО ДОСТУПНЫМ ЯЗЫКОМ</b>\n\n' \
           '<b>✅ КОМЬЮНИТИ</b>\n\nПодкасты, созвоны, приглашение топовых экспертов в разных' \
           'нишах. Ответы на вопросы и чат единомышленников.\nТЫ - не один с тобой братство!\n\n' \
           '<b>❗️В ИТОГЕ ТЫ ДРУГОЙ ЧЕЛОВЕК❗️</b>\n\n<del>Я не умею зарабатывать, я не умею знакомится с девушками, я ' \
           'не умею вести себя в обществе, я не уверен в себе, мне плохо мне грустно, у меня ничего не получится' \
           '</del>\n\n<b>ЖДУ ТЕБЯ В КЛУБЕ 👇👇👇</b>'
    return {'text': text}


async def months_save(clb: CallbackQuery, button: Button, dialog_manager: DialogManager):
    print(clb.data)
    if clb.data == '2_month':
        dialog_manager.dialog_data['months'] = 2
    elif clb.data.startswith('6'):
        dialog_manager.dialog_data['months'] = 6
    else:
        dialog_manager.dialog_data['months'] = 12

    await dialog_manager.switch_to(state=startSG.subscription)


async def check_cryptopay(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    user: User = dialog_manager.middleware_data.get('event_from_user')
    bot: Bot = dialog_manager.middleware_data.get('bot')
    date = dialog_manager.dialog_data.get('months')
    # Добавить ценники
    print(bot)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text='Да', callback_data='yes'),
            InlineKeyboardButton(text='Нет', callback_data='no')
        ]]
    )
    text = f'<b>Заявка на проверку оплаты по криптовалюте</b>\n' \
           f'Данные о заявке:\nОтправленное сообщение: {text}\n' \
           f'Дата действия подписки (месяцы): {date}\n' \
           f'Данные об отправителе:\n   Имя: {user.full_name if user.full_name else "Не указанно"}\n' \
           f'   Айди отправителя: {user.id} (Требуется в технических целях)\n' \
           f'   Username: {user.username if user.username else "Отсутствует"}\n\n' \
           f'Подтверждаете ли вы наличие оплаты юзера?'
    try:
        for admin_id in config.bot.admin_ids:
            await bot.send_message(admin_id, text=text, reply_markup=keyboard)
    except Exception as err:
        print(err)
    await msg.answer('Ваша заявка была отправлена админу, после подтверждения оплаты вы будете добавлены в канал')
    await dialog_manager.done()


async def check_cardpay(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    user: User = dialog_manager.middleware_data.get('event_from_user')
    bot: Bot = dialog_manager.middleware_data.get('bot')
    date = dialog_manager.dialog_data.get('months')
    # Добавить ценники
    text = f'<b>Заявка на проверку оплаты по карте</b>\n' \
           f'Данные о заявке:\n' \
           f'Дата действия подписки (месяцы): {date}\n' \
           f'Данные об отправителе:\n   Имя: {user.full_name if user.full_name else "Не указанно"}\n' \
           f'   Айди отправителя: {user.id} (Требуется в технических целях)\n' \
           f'   Username: {user.username if user.username else "Отсутствует"}\n\n' \
           f'Подтверждаете ли вы наличие оплаты юзера?'

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text='Да', callback_data='yes'),
            InlineKeyboardButton(text='Нет', callback_data='no')
        ]]
    )

    try:
        for admin_id in config.bot.admin_ids:
            await bot.send_photo(chat_id=admin_id, photo=msg.photo[-1].file_id, caption=text, reply_markup=keyboard)
    except Exception as err:
        print(err)
    await msg.answer('Ваша заявка была отправлена админу, после подтверждения оплаты вы будете добавлены в канал')
    await dialog_manager.done()
