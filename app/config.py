class Config:
    MONGODB_SETTINGS = {
        'db': 'assignments',
        'host': 'mongodb://admin:admin@localhost:27017/assignments'
    }
    JWT_SECRET_KEY = 'sua_chave_secreta'
