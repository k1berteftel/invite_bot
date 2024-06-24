from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ChatInviteLink
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.action_data_class import DataInteraction
from database.model import UsersTable
from utils.schedulers_functions import check_sub
from config_data.config import load_config, Config
from states.state_groups import startSG


chat_id = '-1002172546648'
config: Config = load_config()


user_router = Router()


@user_router.message(CommandStart())
async def start_dialog(msg: Message, dialog_manager: DialogManager, session: DataInteraction):
    #users = await session.get_users()
    await session.add_user(user_id=msg.from_user.id)
    await dialog_manager.start(state=startSG.start, mode=StartMode.RESET_STACK)


@user_router.callback_query(F.data == 'yes')
async def confirm_pay(clb: CallbackQuery, bot: Bot, session: DataInteraction, scheduler: AsyncIOScheduler):
    await clb.answer()
    if clb.message.text:
        user_id = int(clb.message.text.split('отправителя:')[1][0:11:].strip())
        date = int(clb.message.text.split('(месяцы):')[1][0:3:].strip())
    else:
        user_id = int(clb.message.caption.split('отправителя:')[1][0:11:].strip())
        date = int(clb.message.caption.split('(месяцы):')[1][0:3:].strip())

    await session.add_sub(user_id, date)
    if not scheduler.get_job(job_id=str(user_id)):
        print('scheduler start work')
        scheduler.add_job(check_sub, 'interval',
                          args=[user_id, bot, scheduler, session], minutes=1, id=str(user_id))

    await clb.message.delete()
    await clb.message.answer(text='Заявка одобрена')

    link: ChatInviteLink = await bot.create_chat_invite_link(chat_id=chat_id, member_limit=1)  # рандомный чат
    await bot.send_message(chat_id=user_id, text=f'Заявка была успешно одобрена\nВаша пригласительная ссылка:{link.invite_link}')


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

@user_router.message(F.photo)
async def get_photo(msg: Message):
    await msg.answer(text=msg.photo[-1].file_id)