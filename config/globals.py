import os
from dotenv import load_dotenv

load_dotenv()

# ENV VARS
TG_BOT_KEY = os.getenv("TG_BOT_KEY")
OR_API_KEY = os.getenv("OR_API_KEY")
NGROK_URL = os.getenv("NGROK_URL")
WEBHOOK_URL = f"{NGROK_URL}/webhook/{TG_BOT_KEY}"
BACKEND_API_URL = os.getenv("BACKEND_API_URL")
