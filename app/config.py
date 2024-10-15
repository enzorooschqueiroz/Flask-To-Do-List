import os 
from dotenv import load_dotenv


load_dotenv()


class Config:
    MONGODB_SETTINGS = {
        'host': os.getenv('MONGO_DB')
    }
    JWT_SECRET_KEY = os.getenv('JWT_TOKEN')
