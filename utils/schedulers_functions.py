import datetime
import logging

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.action_data_class import DataInteraction

from utils.datefunctions import compare_dates

logger = logging.getLogger(__name__)

chat_id = '-1002172546648'


async def check_sub(user_id: int, bot: Bot, scheduler: AsyncIOScheduler, session: DataInteraction):
    date: datetime.datetime = await session.get_sub_date(user_id)
    days = compare_dates(date)
    if days <= 0:
        await bot.send_message(user_id, text='Подписка к сожалению подошла к концу, вы будете удаленны из приватки')
        await bot.ban_chat_member(chat_id, user_id)
        await bot.unban_chat_member(chat_id, user_id)
        await session.set_extension(user_id)
        scheduler.remove_job(str(user_id))
        return
    if days == 5:
        await bot.send_message(user_id, text=f'Ваша подписка к сожалению подходит к концу, осталось всего 5 дней\n'
                                             f'Чтобы остаться в приватке пожалуйста продлите подписку')
    if days == 1:
        await bot.send_message(user_id, text='До конца подписки остался всего один день, чтобы и дальше оставаться в приватке'
                                             'пожалуйста продлите подписку')
