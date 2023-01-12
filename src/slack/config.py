import os
from src.constants import ProductsKeys

from dotenv import load_dotenv

load_dotenv()

class Config():
    SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN', "")