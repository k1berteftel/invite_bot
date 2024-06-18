from aiogram import Router, F
from aiogram.types import ChatJoinRequest

join_router = Router()

@join_router.chat_join_request()
async def confirm_join(request: ChatJoinRequest):
    await request.approve()
    await request.bot.send_message(request.from_user.id, text='Заявка была успешно принята')