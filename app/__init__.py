from flask import Flask
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
import redis
from .routes.assignment_routes import assignment_bp
from .routes.user_routes import user_bp
from .config import Config
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

db = MongoEngine()



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    
    db.init_app(app)
    
    jwt = JWTManager(app)

    app.register_blueprint(assignment_bp)
    app.register_blueprint(user_bp)

    return app
