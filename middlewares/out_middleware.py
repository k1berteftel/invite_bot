from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


class PrivateMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        if data["event_chat"].type != "private":
            return

        result = await handler(event, data)
        return result