import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, requests, status

from ai_api import OpenRouterAPIWrapper
from config.globals import OR_API_KEY, TG_BOT_KEY, WEBHOOK_URL
from bot import bot
from bot.handlers import Router
from logs import Logger

ai = OpenRouterAPIWrapper(model="mistralai/mistral-7b-instruct", key=OR_API_KEY)

logger = Logger()
router = Router(bot, TG_BOT_KEY, ai, logger)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if bot:
        response = await bot.get_webhook_info()
        await logger.log(f"Webhook info: {response}", logger.DEBUG)
        if response.url != WEBHOOK_URL:
            await bot.set_webhook(url=WEBHOOK_URL)

        yield
    else:
        yield


app = FastAPI(lifespan=lifespan)


@app.post("/")
async def read_root():
    return status.HTTP_200_OK


@app.post("/webhook/{bot_token}")
async def webhook(bot_token, request: requests.Request):
    data = await request.json()

    if bot_token != TG_BOT_KEY:
        await logger.log(
            f"Someone connected their bot to this webhook. Endpoint received this: {data}. Request was successfully dodged!",
            logger.INFO,
        )
        return status.HTTP_400_BAD_REQUEST

    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    is_bot = data["message"]["from"]["is_bot"]
    await logger.log(__name__, logger.DEBUG)

    try:
        await logger.log(
            f'{"Bot" if is_bot else "User"} sent this: {data}', logger.DEBUG
        )
        await router.handle(data)
    except Exception as e:
        await logger.log(
            f"Could not handle this message: {data}. Error: {e}", logger.ERROR
        )
        await bot.send_message(
            chat_id=data["message"]["from"]["id"],
            text=f"Unhandled error `{e}`.\nMessage:\n```json\n{json_data}\n```",
            parse_mode="Markdown",
        )

    return status.HTTP_200_OK
