from telethon.sync import TelegramClient
import asyncio


api_id = 9238838
api_hash = "b65e9edfabe1c645a0d101543f065e89"
bot_token = '7402389726:AAHhvumrmEpcF1yHG-BCtn_0T6YEQ5RbqQk'

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)


def get_chat_members(chat_id: int) -> list[int]:
    chat_members = []
    users = bot.iter_participants(chat_id)
    for user in users:
        if not user.deleted:
            print(user.id)
            chat_members.append(user.id)
    return chat_members


def upload_users(user_ids: list[int]):
    users = bot.iter_participants(1002172546648)
    with open('chat_users.log', 'a', encoding='utf-8') as f:
        for user in users:
            if user.id in user_ids:
                f.write(f'{user.__dict__}\n\n')
