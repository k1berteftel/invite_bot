import datetime
import logging

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.model import UsersTable
from database.action_data_class import DataInteraction
from utils.datefunctions import compare_dates

logger = logging.getLogger(__name__)

chats: list[int] = [-1002172546648, -1002178917347, -1002355796294, -1002394200904, -1002280330146, -1002383199495, -1002393214270]

photo_1 = 'AgACAgIAAxkBAAIC4GZ639U2Dn1A83rrnRsbFK1iSu47AAKy3DEbLjTZSz0y-f5N-f2PAQADAgADeQADNQQ'
photo_2 = 'AgACAgIAAxkBAAIC4mZ64CR-N0ynmOBjf9k9HNuHoTFKAAK03DEbLjTZSzdOG3mXddFHAQADAgADeQADNQQ'
photo_3 = 'AgACAgIAAxkBAAIC5GZ64CislFkkP5mn5n7xE0cOzPmBAAK13DEbLjTZS1ONYJeATYd4AQADAgADeQADNQQ'

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text='Продлить подписку', callback_data='extension')
    ]]
)


async def check_sub(user_id: int, bot: Bot, scheduler: AsyncIOScheduler, session: DataInteraction):
    date: datetime.datetime = await session.get_sub_date(user_id)
    days = compare_dates(date)
    if days <= 0:
        try:
            await bot.send_photo(user_id, photo=photo_2, reply_markup=keyboard,
                                 caption='<b>Срок вашей подписки подошёл к концу.</b>\n\n'
                                         'Для возврата в сообщество <b>продлите подписку</b> 👇')
            for chat in chats:
                try:
                    await bot.ban_chat_member(chat, user_id)
                    await bot.unban_chat_member(chat, user_id)
                except Exception:
                    ...
            await session.add_sub(user_id, None)
            await session.set_extension(user_id)
            scheduler.remove_job(str(user_id))
        except Exception as err:
            print(err)
        return
    if days == 5:
        try:
            await bot.send_photo(user_id, photo=photo_1, reply_markup=keyboard,
                                 caption=f'<b>До окончания подписки осталось 5 дней.</b>\n\n'
                                         f'Чтобы и дальше продолжать оставаться в сообществе необходимо <b>продлить подписку</b> 👇')
        except Exception as err:
            print(err)

    if days == 1:
        try:
            await bot.send_photo(user_id, photo=photo_3, reply_markup=keyboard,
                                 caption='<b>До окончания подписки остался 1 день.</b>\n\n'
                                         'Чтобы и дальше продолжать оставаться в сообществе необходимо <b>продлить подписку</b> 👇')
        except Exception as err:
            print(err)


async def ban_chat_members(bot: Bot, session: DataInteraction, chats: list[dict], scheduler: AsyncIOScheduler):
    subs: list[UsersTable] = await session.get_subscriptions()
    subs = [i.user_id for i in subs]
    for chat in chats:
        for member in chat['users']:
            if member not in subs:
                try:
                    await bot.ban_chat_member(chat['chat_id'], member)
                    await bot.unban_chat_member(chat['chat_id'], member)
                except Exception as err:
                    print(err)
    scheduler.remove_job(job_id='clean_chats')