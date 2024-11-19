import os
from dotenv import load_dotenv

load_dotenv()


ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')


if ENCRYPTION_KEY is None:
    raise ValueError("ENCRYPTION_KEY is not set in the .env file.")
