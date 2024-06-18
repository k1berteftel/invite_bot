from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ChatInviteLink
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession

from database.action_data_class import DataInteraction
from config_data.config import load_config, Config
from states.state_groups import startSG


chat_id = 234831248273
config: Config = load_config()


user_router = Router()


@user_router.message(CommandStart())
async def start_dialog(msg: Message, dialog_manager: DialogManager, session: DataInteraction):
    await session.add_user(user_id=msg.from_user.id)
    await dialog_manager.start(state=startSG.start, mode=StartMode.RESET_STACK)


@user_router.callback_query(F.data == 'yes')
async def confirm_pay(clb: CallbackQuery, bot: Bot):
    await clb.answer()
    if clb.message.text:
        user_id = int(clb.message.text.split('отправителя:')[1][0:11:].strip())
        date = int(clb.message.text.split('(месяцы):')[1][0:3:].strip())
    else:
        user_id = int(clb.message.caption.split('отправителя:')[1][0:11:].strip())
        date = int(clb.message.caption.split('(месяцы):')[1][0:3:].strip())
    print(user_id)
    print(date)
    await clb.message.delete()
    await clb.message.answer(text='Заявка одобрена')

    #  Занос в базу данных
    link: ChatInviteLink = await bot.create_chat_invite_link(chat_id=chat_id, member_limit=1,)  # рандомный чат
    await bot.send_message(chat_id=user_id, text=f'Заявка была успешно одобрена\nВаша пригласительная ссылка:{link}')


@user_router.callback_query(F.data == 'no')
async def cancel_pay(clb: CallbackQuery, bot: Bot):
    await clb.answer()
    if clb.message.text:
        user_id = int(clb.message.text.split('отправителя:')[1][0:11:].strip())
    else:
        user_id = int(clb.message.caption.split('отправителя:')[1][0:11:].strip())

    await clb.message.delete()
    await clb.message.answer(text='Заявка была отклонена')
    await bot.send_message(chat_id=user_id, text='Заявка была отклонена\nДля связи с поддержкой писать @username')