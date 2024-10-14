from flask import Flask
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
import redis
from .routes.assignment_routes import assignment_bp
from .routes.user_routes import user_bp
from .config import Config

db = MongoEngine()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializando MongoDB e Redis
    db.init_app(app)
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    
    # Configurando JWT
    jwt = JWTManager(app)

    # Registrando Blueprints
    app.register_blueprint(assignment_bp)
    app.register_blueprint(user_bp)

    return app
