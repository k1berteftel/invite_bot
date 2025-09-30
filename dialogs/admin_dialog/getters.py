import os
from aiogram import Bot
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import MessageInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from states.state_groups import adminSG
from database.action_data_class import DataInteraction
from database.model import UsersTable
from utils.tables_functions import get_table
from utils.schedulers_functions import ban_chat_members
from utils.chat_functions import get_chat_members

chats = [-1002172546648, -1002178917347, -1002355796294, -1002394200904, -1002280330146, -1002383199495, -1002393214270]

chat_members = {
    'users': get_chat_members(chats[0]),
    'chat_id': chats[0]
}
channel_members = {
    'users': get_chat_members(chats[1]),
    'chat_id': chats[1]
}

chat_members_1 = {
    'users': get_chat_members(chats[2]),
    'chat_id': chats[2]
}

chat_members_2 = {
    'users': get_chat_members(chats[3]),
    'chat_id': chats[3]
}

chat_members_3 = {
    'users': get_chat_members(chats[4]),
    'chat_id': chats[4]
}

chat_members_4 = {
    'users': get_chat_members(chats[5]),
    'chat_id': chats[5]
}

chat_members_5 = {
    'users': get_chat_members(chats[6]),
    'chat_id': chats[6]
}


async def clean_channels(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    bot: Bot = dialog_manager.middleware_data.get('bot')
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    scheduler: AsyncIOScheduler = dialog_manager.middleware_data.get('scheduler')
    chats = [chat_members, channel_members, chat_members_1, chat_members_2, chat_members_3, chat_members_4, chat_members_5]
    scheduler.add_job(
        ban_chat_members,
        'interval',
        args=[bot, session, chats, scheduler],
        id='clean_chats',
        seconds=20
    )
    await clb.answer('Старт чистки')


async def subs_malling_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data['sub'] = True
    await dialog_manager.switch_to(adminSG.get_mail)


async def get_subs_static(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    data: list[UsersTable] = await session.get_base()
    columns = []
    for i in data:
        if i.subscription:
            columns.append(
                [
                    int(i.id),
                    i.name,
                    i.username,
                    int(i.user_id),
                    str(i.entry) if i.entry else i.entry,
                    str(i.subscription) if i.subscription else i.subscription,
                    i.extension
                ]
            )
    columns.insert(0, ['Идентификатор', 'Имя пользователя', 'Юзернейм пользователя', 'id пользователя', 'Дата запуска бота', 'Конечная дата подписки', 'Продления'])
    table = get_table(columns)
    await clb.message.answer_document(FSInputFile(table))

    try:
        os.remove(table)
    except Exception as err:
        print(err)


async def get_days(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    try:
        days = int(text)
    except Exception:
        await message.answer('Вы вели количество дней не корректно')
        return
    user: UsersTable = dialog_manager.dialog_data.get('user')
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    await session.add_sub_days(user.user_id, days)
    await message.answer('Дни были успешно добавлены к подписке юзера')
    dialog_manager.dialog_data.clear()
    await dialog_manager.switch_to(state=adminSG.main)


async def sub_getter(dialog_manager: DialogManager, **kwargs):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    user: UsersTable = dialog_manager.dialog_data.get('user')
    sub_date = await session.get_sub_date(user.user_id)
    if not sub_date:
        sub = False
        sub_date = '❌Отсутствует'
    else:
        sub = True
        sub_date = f'✅Присутствует\nПодписка до: {str(sub_date).split(" ")[0].strip()}'

    return {
        'name': user.name,
        'username': user.username,
        'id': user.user_id,
        'sub_date': sub_date,
        'sub': sub,
        'not_sub': not sub
    }


async def get_user_id(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    try:
        text = int(text)
    except:
        await message.answer('Формат веденного айди юзера неверен')
        return
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    user = await session.get_user(text)
    if not user:
        await message.answer('Данного юзера нет в боте')
        return
    dialog_manager.dialog_data['user'] = user
    await dialog_manager.switch_to(state=adminSG.user_info)


async def get_database(clb: CallbackQuery, btn: Button, dialog_manager: DialogManager, **kwargs):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    data: list[UsersTable] = await session.get_base()
    columns = []
    for i in data:
        columns.append(
            [
                int(i.id),
                i.name,
                i.username,
                int(i.user_id),
                str(i.entry) if i.entry else i.entry,
                str(i.subscription) if i.subscription else i.subscription,
                i.extension
            ]
        )
    columns.insert(0, ['Идентификатор', 'Имя пользователя', 'Юзернейм пользователя', 'id пользователя', 'Дата запуска бота', 'Конечная дата подписки', 'Продления'])
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


async def mail_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data['audience'] = clb.data.split('_')[0]
    await dialog_manager.switch_to(adminSG.get_mail)


async def save_message(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['message'] = message
    await dialog_manager.switch_to(adminSG.malling)


async def send_message(clb: CallbackQuery, btn: Button, dialog_manager: DialogManager, **kwargs):
    message: Message = dialog_manager.dialog_data.get('message')
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    audience = dialog_manager.dialog_data.get('audience')
    if audience == 'all':
        users = await session.get_users()
    elif audience == 'subs':
        users = [user.user_id for user in await session.get_subscriptions()]
    else:
        users = await session.get_users()
        sub_users = await session.get_subscriptions()
        users = [user for user in users if user not in [sub_user.user_id for sub_user in sub_users]]
    print(users)
    for user in users:
        try:
            await message.send_copy(
                chat_id=user
            )
        except Exception as err:
            print(err)
    await clb.answer('Рассылка прошла успешно')
    await dialog_manager.start(state=adminSG.main, mode=StartMode.RESET_STACK)
