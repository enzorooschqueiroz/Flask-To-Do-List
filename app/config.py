import os 
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_SETTINGS = {
        'host': os.getenv('MONGODB_KEY')
    }
    JWT_SECRET_KEY = ''
