import os 
from dotenv import load_dotenv


load_dotenv()


class Config:
    MONGODB_SETTINGS = {
        'host': os.getenv('MONGO_DB')
    }
    JWT_SECRET_KEY = os.getenv('JWT_TOKEN')

    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')