import json
import random

import httpx
from telegram import Bot

from ai_api import OpenRouterAPIWrapper
from logs import Logger
from bot.handlers import BaseHandler


class MessageHandler:
    def __init__(
        self, tg_bot: Bot, key: str, or_wrapper: OpenRouterAPIWrapper, logger: Logger
    ) -> None:
        self.bot = tg_bot

        self.api_key = key
        self.or_wrapper = or_wrapper
        self.logger = logger
        self.greets = [
            "Gmorning",
            "Good afternoon",
            "Good day",
            "Good evening",
            "Good morning",
            "Good to see you",
            "Greeting",
            "Greetings",
            "G’day",
            "Hello",
            "Hello there",
            "Helloo",
            "Hellooo",
            "Hey",
            "Hey there",
            "Heyya",
            "Heyya there",
            "Hi",
            "Hi there",
            "Hiya",
            "Hiya there",
            "How are things",
            "How are you",
            "How are you doing",
            "How has life been treating you",
            "How have you been",
            "How is everything",
            "How is everything going",
            "How is it going",
            "How're things",
            "How're you",
            "How's everything going",
            "How's it goin",
            "How's it goin'",
            "How's it going",
            "How's life been treating you",
            "How've you been",
            "Howdy",
            "Its good seeing you",
            "Morning",
            "What is cracking",
            "What is good",
            "What is happening",
            "What is new",
            "What is up",
            "What's cracking",
            "What's good",
            "What's happening",
            "What's new",
            "What's up",
        ]

    async def handle(self, data: dict[str, any]) -> None:
        message_text = data["message"].get("text")

        if not message_text:
            await self.logger.log(
                f"Seems like message didn't contain text. Data: {data}, Error: {e}",
                self.logger.DEBUG,
            )

        if "photo" in data["message"].keys():
            await self._handle_photo(data)

    async def _handle_message(self, data: dict[str, any]) -> None:
        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        message_text = data["message"]["text"]
        for greet in self.greets:
            if greet.lower() in message_text.lower():
                await self.bot.send_message(
                    chat_id=data["message"]["from"]["id"],
                    text=f"{self.greets[random.randint(0, len(self.greets) - 1)]}! I'm a bot. How are you?",
                    parse_mode="Markdown",
                )
                break

    async def _handle_photo(self, data: dict[str, any]) -> None:
        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        photo = await self.get_document(data["message"]["photo"][-1]["file_id"])
        await self.bot.send_message(
            chat_id=data["message"]["from"]["id"],
            text=f"Successfully received photo: \n```json\n{json_data}\n```",
            parse_mode="Markdown",
        )
        await self.bot.send_photo(chat_id=data["message"]["from"]["id"], photo=photo)

    async def _handle_video(self, data: dict[str, any]) -> None:
        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        video = await self.get_document(data["message"]["video"][-1]["file_id"])
        await self.bot.send_message(
            chat_id=data["message"]["from"]["id"],
            text=f"Successfully received video: \n```json\n{json_data}\n```",
            parse_mode="Markdown",
        )
        await self.bot.send_video(chat_id=data["message"]["from"]["id"], video=video)

    async def _log_message(self, data: dict[str, any]) -> None:
        with open("./messages.json", "r") as f:
            json_data = json.load(f)

        json_data["messages"].append(data)

        with open("./messages.json", "w+") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)

    async def get_document(self, file_id: str) -> bytes | None:
        url = f"https://api.telegram.org/bot{self.api_key}/getFile?file_id={file_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            filepath = response.json()["result"]["file_path"]

            response = await client.get(
                f"https://api.telegram.org/file/bot{self.api_key}/{filepath}"
            )
            response.raise_for_status()
            return response.content
