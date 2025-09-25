import re

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ChatInviteLink, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.action_data_class import DataInteraction
from database.model import UsersTable
from utils.schedulers_functions import check_sub
from config_data.config import load_config, Config
from states.state_groups import startSG


chats: dict[str, int] = {
    '• [ПРИВАТ] БОЙЦОВСКИЙ КУРТ': -1002172546648,
    '• [ПРИВАТ ЧАТ БК] Основа': -1002178917347,
    '• [ПРИВАТ ЧАТ БК] Флудильня': -1002355796294,
    '• [ПРИВАТ] Инвестиции': -1002394200904,
    '• [ПРИВАТ] Новости': -1002280330146,
    '• [ПРИВАТ] Лудка': -1002383199495,
    '• [ПРИВАТ] Саморазвитие': -1002393214270
}
config: Config = load_config()


user_router = Router()


@user_router.message(CommandStart())
async def start_dialog(msg: Message, dialog_manager: DialogManager, session: DataInteraction):
    #users = await session.get_users()
    await session.add_user(user_id=msg.from_user.id, username=msg.from_user.username if msg.from_user.username else '', name=msg.from_user.full_name)
    await dialog_manager.start(state=startSG.start, mode=StartMode.RESET_STACK)


@user_router.callback_query(F.data == 'yes')
async def confirm_pay(clb: CallbackQuery, bot: Bot, session: DataInteraction, scheduler: AsyncIOScheduler):
    await clb.answer()
    if clb.message.text:
        user = (clb.message.text.split('отправителя:')[1])
        user_id = re.search(r'\d+', user)
        user_id = int(user[user_id.start():user_id.end():])
        date = int(clb.message.text.split('Тариф:')[1][0:3:].strip())
    else:
        user = clb.message.caption.split('отправителя:')[1]
        user_id = re.search(r'\d+', user)
        user_id = int(user[user_id.start():user_id.end():])
        date = int(clb.message.caption.split('Тариф:')[1][0:3:].strip())

    await session.add_sub(user_id, date)
    if not scheduler.get_job(job_id=str(user_id)):
        print('scheduler start work')
        scheduler.add_job(check_sub, 'interval',
                          args=[user_id, bot, scheduler, session], hours=24, id=str(user_id))

    await clb.message.delete()
    await clb.message.answer(text='Заявка одобрена')

    buttons = []
    for chat, chat_id in chats.items():
        try:
            link: ChatInviteLink = await bot.create_chat_invite_link(chat_id=chat_id, creates_join_request=True)
        except Exception:
            continue
        buttons.append([InlineKeyboardButton(text=chat, url=link.invite_link)])
    await bot.send_photo(
        photo=FSInputFile(path='Фон.jpg'),
        chat_id=user_id,
        caption=f'💬 Нажмите на кнопки снизу, чтобы присоединиться ко всей экосистеме '
                f'закрытого сообщества «Бойцовский Курт» 👇👇👇',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )


@user_router.callback_query(F.data == 'no')
async def cancel_pay(clb: CallbackQuery, bot: Bot):
    await clb.answer()
    if clb.message.text:
        user_id = int(clb.message.text.split('отправителя:')[1][0:11:].strip())
    else:
        user_id = int(clb.message.caption.split('отправителя:')[1][0:11:].strip())

    await clb.message.delete()
    await clb.message.answer(text='Заявка была отклонена')
    await bot.send_message(chat_id=user_id, text='Заявка была отклонена\nДля связи с поддержкой писать @gambIer_kurt')


@user_router.callback_query(F.data == 'extension')
async def to_payment(clb: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(state=startSG.sub_date, mode=StartMode.RESET_STACK)


#@user_router.message(F.photo)
#async def get_photo(msg: Message):
#    await msg.answer(text=msg.photo[-1].file_id)