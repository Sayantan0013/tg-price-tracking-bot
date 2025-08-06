import os
from dotenv import load_dotenv

load_dotenv() # loads variables from .env file

BOT_TOKEN = os.getenv("BOT_TOKEN","")
ADMIN_ID = int(os.getenv("ADMIN_ID",""))
