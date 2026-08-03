from anthropic import Anthropic
from dotenv import load_dotenv


import os

load_dotenv()

def get_client():
    return Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


