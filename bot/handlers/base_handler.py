from telegram import Bot

from ai_api import OpenRouterAPIWrapper
from logs import Logger


class BaseHandler:
    def __init__(
        self, tg_bot: Bot, key: str, or_wrapper: OpenRouterAPIWrapper, logger: Logger
    ) -> None:
        self.bot = tg_bot

        self.api_key = key
        self.or_wrapper = or_wrapper
        self.logger = logger
