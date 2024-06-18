from aiogram import Bot
from aiogram.types import Message, CallbackQuery, User, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput

from states.state_groups import startSG
from config_data.config import Config, load_config

config: Config = load_config()

async def menu(event_from_user: User, **kwargs):
    admin = False
    if event_from_user.id in config.bot.admin_ids:
        admin = True
    return {'admin': admin}


async def months_save(clb: CallbackQuery, button: Button, dialog_manager: DialogManager):
    print(clb.data)
    if clb.data == '1_month':
        dialog_manager.dialog_data['months'] = 1
    elif clb.data.startswith('6'):
        dialog_manager.dialog_data['months'] = 6
    else:
        dialog_manager.dialog_data['months'] = 12

    await dialog_manager.switch_to(state=startSG.subscription)


async def check_cryptopay(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    user: User = dialog_manager.middleware_data.get('event_from_user')
    bot: Bot = dialog_manager.middleware_data.get('bot')
    date = dialog_manager.dialog_data.get('months')
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
    await dialog_manager.switch_to(state=startSG.start)


async def check_cardpay(msg: Message, message_input: MessageInput, dialog_manager: DialogManager):
    user: User = dialog_manager.middleware_data.get('event_from_user')
    bot: Bot = dialog_manager.middleware_data.get('bot')
    date = dialog_manager.dialog_data.get('months')

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
    await dialog_manager.switch_to(state=startSG.start)
