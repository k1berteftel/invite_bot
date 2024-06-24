import os
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from states.state_groups import adminSG
from database.action_data_class import DataInteraction
from database.model import UsersTable
from utils.tables_functions import get_table


async def get_database(clb: CallbackQuery, btn: Button, dialog_manager: DialogManager, **kwargs):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    data: list[UsersTable] = await session.get_base()
    columns = []
    for i in data:
        columns.append(
            [
                int(i.id),
                int(i.user_id),
                str(i.entry) if i.entry else i.entry,
                str(i.subscription) if i.subscription else i.subscription,
                i.extension
            ]
        )
    columns.insert(0, ['Идентификатор', 'id пользователя', 'Дата запуска бота', 'Конечная дата подписки', 'Продления'])
    table = get_table(columns)
    await clb.message.answer_document(FSInputFile(table))

    try:
        os.remove(table)
    except Exception as err:
        print(err)


async def send_static(clb: CallbackQuery, btn: Button, dialog_manager: DialogManager, **kwargs):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    subs = await session.get_active_subscriptions()
    new_users = await session.get_new_users()
    extensions = await session.get_extensions()
    text = f'Юзеров с активной подпиской: {subs}\n' \
           f'Юзеров зашло в этом месяце в бота: {new_users}\n' \
           f'Всего юзеров продлевало подписку: {extensions}'
    await clb.message.answer(text=text)


    # логика Отправки статистики
    # await clb.message.answer(f'Активных пользователей: {count}\nЗашло сегодня: {today}')


async def save_message(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['message'] = message
    await dialog_manager.switch_to(adminSG.malling)


async def send_message(clb: CallbackQuery, btn: Button, dialog_manager: DialogManager, **kwargs):
    message: Message = dialog_manager.dialog_data.get('message')
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    users = await session.get_users()
    print(users)
    for user in users:
        try:
            await message.send_copy(user)
        except Exception as err:
            print(err)
    await clb.answer('Рассылка прошла успешно')
    await dialog_manager.start(state=adminSG.main, mode=StartMode.RESET_STACK)
