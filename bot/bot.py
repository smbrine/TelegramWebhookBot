from telegram import Bot

from config.globals import TG_BOT_KEY
from security import BotSecurity

bot = Bot(token=TG_BOT_KEY)

allowed_users = [855235544]
clearance = BotSecurity(allowed_users)
