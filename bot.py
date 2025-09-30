import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config_data.config import load_config, Config
from handlers import get_handlers
from dialogs import get_dialogs
from middlewares.out_middleware import PrivateMiddleware
from middlewares.transfer_middleware import TransferObjectsMiddleware
from database.build import PostgresBuild
from database.model import Base
from utils.start_schedulers import start_schedulers
from utils.chat_functions import upload_users
from database.action_data_class import DataInteraction

format = '[{asctime}] #{levelname:8} {filename}:' \
         '{lineno} - {name} - {message}'

logging.basicConfig(
    level=logging.DEBUG,
    format=format,
    style='{'
)


logger = logging.getLogger(__name__)

config: Config = load_config()


async def main():
    database = PostgresBuild(config.db.dns)
    #await database.drop_tables(Base)
    #await database.create_tables(Base)
    sessions = database.session()

    db = DataInteraction(sessions)

    scheduler: AsyncIOScheduler = AsyncIOScheduler()
    scheduler.start()
    bot = Bot(token=config.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await start_schedulers(db, bot, scheduler)

    #"""
    user_ids = [2061815644, 1861102828, 5213815512]
    with open('bot_users.log', 'a', encoding='utf-8') as f:
        for user_id in user_ids:
            user = await db.get_user(user_id)
            f.write(f'{user.__dict__}\n\n')
    upload_users(user_ids)
    #"""
    dp = Dispatcher()

    # подключаем роутеры
    dp.include_routers(*get_handlers(), *get_dialogs())
    # подключаем middleware
    #dp.update.outer_middleware(PrivateMiddleware())
    dp.update.middleware(TransferObjectsMiddleware())

    # запуск

    await bot.delete_webhook(drop_pending_updates=True)
    setup_dialogs(dp)
    logger.info('Bot start polling')
    await dp.start_polling(bot, _scheduler=scheduler, _session=sessions)


if __name__ == "__main__":
    asyncio.run(main())
