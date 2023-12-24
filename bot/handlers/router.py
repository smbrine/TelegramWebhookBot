from telegram import Bot

from ai_api import OpenRouterAPIWrapper
from bot.handlers import CommandHandler, MessageHandler
from logs import Logger


class Router:
    def __init__(
        self, tg_bot: Bot, key: str, or_wrapper: OpenRouterAPIWrapper, logger: Logger
    ) -> None:
        self.bot = tg_bot

        self.api_key = key
        self.or_wrapper = or_wrapper
        self.logger = logger

    async def handle(self, data: dict[str, any]) -> None:
        if not data:
            return
        message_text = data["message"].get("text")
        if message_text:
            if message_text.startswith("/"):
                await CommandHandler(
                    self.bot, self.api_key, self.or_wrapper, self.logger
                ).handle(data)
            else:
                await MessageHandler(
                    self.bot, self.api_key, self.or_wrapper, self.logger
                ).handle(data)

        else:
            await self.logger.log(
                f"Seems like message didn't contain text. Data: {data}",
                self.logger.DEBUG,
            )
            await self.bot.send_message(
                chat_id=data["message"]["from"]["id"],
                text=f"I don't know how to reply to this message.",
                reply_to_message_id=data["message"]["message_id"],
            )
