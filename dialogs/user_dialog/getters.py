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
        price = 89
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


async def crypto_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data['lan'] = clb.data
    await dialog_manager.switch_to(startSG.crypto)


async def crypto_getter(dialog_manager: DialogManager, **kwargs):
    months = dialog_manager.dialog_data.get('months')
    lan = dialog_manager.dialog_data.get('lan')
    print(months)
    if months == 2:
        price = 89
    elif months == 6:
        price = 229
    else:
        price = 429
    if lan == 'TRC20':
        link = 'TLhS4daX8Yj21PGYDAEgsvjz21q5gwCVff'
    elif lan == 'BEP20':
        link = '0x78e3ed9cc71faA4053325363eE15a7c081750984'
    else:
        link = '0x32fafa6c45bb17ddb39cd9e682701751070c356eb2ef8b2a1d07f9749459dd49'
    dialog_manager.dialog_data['price'] = price
    return {
        'price': price,
        'lan': lan,
        'link': link
    }


async def sub_getter(session: DataInteraction, event_from_user: User, **kwargs):
    sub = await session.get_sub_date(event_from_user.id)
    if sub:
        is_sub = f'✅Присутствует\n<b>Дата окончания подписки</b>: {str(sub).split(" ")[0].strip()}\n'
    else:
        is_sub = '❌Отсутствует'
    return {
        'username': event_from_user.username,
        'name': event_from_user.full_name if event_from_user.full_name else 'Отсутствует',
        'id': event_from_user.id,
        'sub': is_sub
    }


async def menu(event_from_user: User, **kwargs):
    admin = False
    if event_from_user.id in config.bot.admin_ids:
        admin = True
    image_id = "AgACAgIAAxkBAAIBw2Z3BDt2vUYgAfpH2UnNzBZ76xkfAAK33jEbWRa4Sx87TPnSUD6jAQADAgADeQADNQQ"  # Your file_id
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
    text = ('<b>Закрытый Клуб по Заработку Бойцовский Курт</b> 👋\n\n'
            'Здесь онлайн формат. Бабки из любой точки мира.\nЗдесь развиваются как физически, так и ментально.'
            '\n\n<b>1.</b> ЛУТАЕМ ЗП РОДИТЕЛЕЙ В 3 ШАГА <a href="https://t.me/locked_club/17"><b>[ПРУФ]</b></a>\n'
            '\n<b>2.</b> ДОМИНИРУЕМ ВМЕСТЕ <a href="https://t.me/locked_club/2"><b>[ПРУФ]</b></a>\n\n'
            '<b>3.</b> ВЫНОСИМ КРИПТУ НА 5.000.000₽ ЗА 3 ДНЯ <a href="https://t.me/locked_club/27"><b>[ПРУФ]</b></a>'
            '\n\n<b>Твоя личная ответственность — гарантия успеха 🏆</b>')
    return {'admin': admin,
            'text': text,
            'photo': image}


async def about(**kwargs):
    text = ('<b>НАХОДЯСЬ В КЛУБЕ ТЫ ПОЛУЧИШЬ👇</b>\n\n<b>→ ЛЁГКИЙ СТАРТ</b>\n\nДля заработка первого капитала не '
            'нужно иметь профессиональных знаний или особых умений, достаточно лишь знать алгоритм работы.'
            ' И Я ДАМ ТЕБЕ ЕГО.\n\nЗарегистрироваться на сайте или скачать крипто-тапалку, уделяя ей по 5 минут '
            'каждый день — уже твой шанс зафармить минимум 4000-7000₽ как с куста.\n\n<b>→ ЭТО РЕАЛЬНЫЙ ЗАРАБОТОК В '
            'ИНТЕРНЕТЕ</b>\n\nУ тебя уже есть всё, чтобы начать, буквально из любой точки мира. Твои инструменты — '
            'телефон/комп + интернет. <b>ВСЁ.</b>\n\n<b>→ УНИВЕРСАЛЬНО ДЛЯ ЛЮБОГО ВОЗРАСТА</b>\n\nНе важно кто ты —'
            ' 14 летний школьник или 83 летний дедок, в криптовалюте эта информация АБСОЛЮТНО никому не нужна. \n'
            'Твой заработок определяется ТОЛЬКО действиями. \n\nСидишь, ничего не делая, и ждёшь бабок с неба? — Удачи.'
            '\nВидишь возможности и ебашишь по ним? — В 16 лет лутаешь 300.000₽.\n\n<b>→ КОМАНДА – ТЫ БОЛЬШЕ НЕ '
            'ОДИН</b>\n\nРядом с тобой будут те, кто уже зарабатывает и знает, как это делать. Здесь не нужно '
            'подстраиваться под общество, прятать амбиции или оправдываться за своё желание зарабатывать. '
            'Ты больше не чужой.\n\n<b>→ ГАЙДЫ, ПОСТЫ и ВИДЕОУРОКИ</b>\n\nЦеннейшая информация МАКСИМАЛЬНО '
            'доступным языком приведёт тебя к стабильному доходу в сфере крипты.\n\nБольше не нужно выживать, '
            'экономя деньги буквально на всём. Крипта действительно кормит и ты убедишься в этом на своём примере.\n'
            '\n<b> 🫵 ХОЧЕШЬ ТАКИХ ЖЕ РЕЗУЛЬТАТОВ? 🫵</b>\n\nКурт [77.000$ за 3 месяца] — '
            '<a href="https://t.me/c/1861980586/204">ОТЗЫВ</a>\nПаша [3.300$ за схему] — '
            '<a href="https://t.me/c/1861980586/261">ОТЗЫВ</a>\nСаша [с 0 до 700$ за месяц] — <a href='
            '"https://t.me/c/1861980586/270">ОТЗЫВ</a>\nДаня [1.000.000₽ в 16 лет] — <a '
            'href="ttps://t.me/c/1861980586/336">ОТЗЫВ</a>\nCотни других результатов людей — <a '
            'href="http://t.me/locked_club">ДОХУЯ ОТЗЫВОВ</a>\n\n<b>ЖДУ ТЕБЯ В НАШЕМ КЛУБЕ 👇👇👇</b>')
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
    price = dialog_manager.dialog_data.get('price')
    # Добавить ценники
    print(bot)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text='Да', callback_data='yes'),
            InlineKeyboardButton(text='Нет', callback_data='no')
        ]]
    )
    text = f'<b>Заявка на проверку оплаты, Криптовалюта</b>\n\n' \
           f'Данные о заявке:\n<b>Transaction ID</b>: {text}\n\n' \
           f'<b>Тариф</b>: {date} месяцев за {price} $\n\n' \
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
    price = dialog_manager.dialog_data.get('price')
    # Добавить ценники
    text = f'<b>Заявка на проверку оплаты, Карта</b>\n\n' \
           f'Данные о заявке:\n<b>Transaction ID</b>: {text}\n\n' \
           f'<b>Тариф</b>: {date} месяцев за {price} $\n\n' \
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
            await bot.send_message(chat_id=admin_id, text=text, reply_markup=keyboard)
    except Exception as err:
        print(err)
    await msg.answer('Ваша заявка была отправлена админу, после подтверждения оплаты вы будете добавлены в канал')
    await dialog_manager.done()
