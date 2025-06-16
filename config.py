from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
KINOPOISK_API_TOKEN = os.getenv("KINOPOISK_API_TOKEN")
