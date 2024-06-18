from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from states.state_groups import adminSG


async def send_static(clb: CallbackQuery, btn: Button, dialog_manager: DialogManager, **kwargs):
    pass
    # логика Отправки статистики
    # await clb.message.answer(f'Активных пользователей: {count}\nЗашло сегодня: {today}')


async def save_message(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['message'] = message
    await dialog_manager.switch_to(adminSG.malling)


async def send_message(clb: CallbackQuery, btn: Button, dialog_manager: DialogManager, **kwargs):
    message: Message = dialog_manager.dialog_data.get('message')
    # Достать из базы данных юзеров
    users = []  # Заглушка
    for user in users:
        try:
            await message.send_copy(user[0])
        except Exception as err:
            print(err)
    await clb.answer('Рассылка прошла успешно')
    await dialog_manager.start(state=adminSG.main, mode=StartMode.RESET_STACK)
