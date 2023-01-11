import os
from src.constants import ProductsKeys

from dotenv import load_dotenv

load_dotenv()

class Config():
    HUBSPOT_TOKEN = os.getenv('HUBSPOT_TOKEN', "")
    HUBSPOT_CONTRACT_OBJECT_TYPE = os.getenv('HUBSPOT_CONTRACT_OBJECT_TYPE', "CONTRACT")
    HUBSPOT_PROJECT_OBJECT_TYPE = os.getenv('HUBSPOT_PROJECT_OBJECT_TYPE', "PROJECT")
    HUBSPOT_USER_ID = os.getenv('HUBSPOT_USER_ID', "1")
    CS_OWNERS_DATA = [
        {
            "email": "alex@growth97.com",
            "products": [
                ProductsKeys.KD_SEO,
                ProductsKeys.KD_ANLT,
                ProductsKeys.KD_CRM,
                ProductsKeys.KD_PROC,
            ]
        },
        {
            "email": "desarrollo.isaac@alotofpipol.com",
            "products": [
                ProductsKeys.KD_WEB,
                ProductsKeys.KD_RRSS,
                ProductsKeys.KD_ECOM
            ]
        }
    ]