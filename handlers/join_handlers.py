from aiogram import Router, F
from aiogram.types import ChatJoinRequest

from database.action_data_class import DataInteraction
from utils.datefunctions import compare_dates


join_router = Router()


@join_router.chat_join_request()
async def confirm_join(request: ChatJoinRequest, session: DataInteraction):
    try:
        sub = await session.get_sub_date(request.from_user.id)
        if sub:
            if compare_dates(sub) > 0:
                await request.approve()
                await request.bot.send_message(request.from_user.id, text='Заявка была успешно принята')
                return
    except Exception as err:
        print(err)
    await request.decline()
