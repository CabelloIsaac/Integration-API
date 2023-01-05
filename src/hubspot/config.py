import os

from dotenv import load_dotenv

load_dotenv()

class Config():
    HUBSPOT_TOKEN = os.getenv('HUBSPOT_TOKEN', "")
    HUBSPOT_CONTRACT_OBJECT_TYPE = os.getenv('HUBSPOT_CONTRACT_OBJECT_TYPE', "CONTRACT")
    HUBSPOT_PROJECT_OBJECT_TYPE = os.getenv('HUBSPOT_PROJECT_OBJECT_TYPE', "PROJECT")
    CS_OWNERS_EMAILS = [
        "desarrollo.isaac@alotofpipol.com",
    ]