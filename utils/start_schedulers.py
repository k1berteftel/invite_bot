import datetime

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.schedulers_functions import check_sub
from database.model import UsersTable
from database.action_data_class import DataInteraction


async def start_schedulers(session: DataInteraction, bot: Bot, scheduler: AsyncIOScheduler):
    users: list[UsersTable] = await session.get_base()
    for user in users:
        if user.subscription and user.subscription > datetime.datetime.now():
            if not scheduler.get_job(job_id=str(user)):
                scheduler.add_job(check_sub, 'interval',
                                  args=[user, bot, scheduler, session], hours=24, id=str(user))
        else:
            await session.add_sub(user.user_id, None)
