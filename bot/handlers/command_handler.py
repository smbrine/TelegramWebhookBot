import json

from ai_api import OpenRouterAPIWrapper
from bot import clearance
from bot.bot import Bot
from bot.handlers import BaseHandler
from logs import Logger


class CommandHandler(BaseHandler):
    def __init__(
        self, tg_bot: Bot, key: str, or_wrapper: OpenRouterAPIWrapper, logger: Logger
    ) -> None:
        super().__init__(tg_bot, key, or_wrapper, logger)

    async def handle(self, data: dict[str, any]) -> None:
        message_text = data["message"].get("text")
        if message_text.startswith("/ask_ai "):
            await self._handle_ask_ai(data)
        elif message_text.startswith("/add_user "):
            await self._handle_add_user(data)
        elif message_text.startswith("/get_users"):
            await self._handle_get_users(data)
        else:
            await self._handle_command(data)

    async def _handle_command(self, data: dict[str, any]) -> None:
        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        await self.bot.send_message(
            chat_id=data["message"]["from"]["id"],
            text=f"I don't know this command yet!",
            parse_mode="Markdown",
            reply_to_message_id=data["message"]["message_id"],
        )

    @clearance.is_allowed
    async def _handle_ask_ai(self, data: dict[str, any]) -> None:
        question = str(data["message"]["text"]).replace("/ask_ai ", "")
        bot_response = await self.or_wrapper.answer(question)
        await self.bot.send_message(
            chat_id=data["message"]["from"]["id"],
            text=bot_response,
            parse_mode="Markdown",
        )
        await logger.log(data, )
    @clearance.is_allowed
    async def _handle_add_user(self, data: dict[str, any]):
        print(data)
        user_id = str(data["message"]["text"]).replace("/add_user ", "")
        clearance.allowed_users.append(int(user_id))
        await self.bot.send_message(
            chat_id=data["message"]["from"]["id"],
            text=f"Successfully added user {user_id} to allowed users",
        )

    async def _handle_get_users(self, data: dict[str, any]) -> None:
        await self.bot.send_message(
            chat_id=data["message"]["from"]["id"],
            text=f"Allowed users: {clearance.allowed_users}",
        )
