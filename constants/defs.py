import os
from dotenv import load_dotenv

load_dotenv()
private_api = os.getenv("API_KEY")
private_account = os.getenv("ACCOUNT_ID")
private_url = os.getenv("OANDA_URL")


API_KEY = private_api
ACCOUNT_ID = private_account
OANDA_URL = private_url