import os

from dotenv import load_dotenv

load_dotenv()

class Config():
    HUBSPOT_TOKEN = os.getenv('HUBSPOT_TOKEN', "")
    CS_OWNERS_EMAILS = [
        "desarrollo.isaac@alotofpipol.com",
    ]