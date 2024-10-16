from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user_model import UserModel
import redis
import json
from bson import ObjectId

user_bp = Blueprint('users', __name__)
redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)


def serialize_object_id(data):
    if isinstance(data, dict):
        return {key: serialize_object_id(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [serialize_object_id(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    return data

@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    if UserModel.objects(user_email=data['user_email']).first():
        return {'message': 'User already exists'}, 400

    hashed_password = generate_password_hash(data['user_password'], method='sha256')

    new_user = UserModel(
        user_name=data['user_name'],
        user_email=data['user_email'],
        user_password=hashed_password
    )
    
    new_user.save()

    user_data = new_user.to_mongo().to_dict()
    user_data = serialize_object_id(user_data)  # Converte ObjectId para string

    redis_client.set(f"user:{new_user.user_email}", json.dumps(user_data))

    return {'message': 'User created successfully'}, 201


@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = UserModel.objects(user_email=data['user_email']).first()

    if not user or not check_password_hash(user.user_password, data['user_password']):
        return {'message': 'Invalid credentials'}, 401

    access_token = create_access_token(identity=user.user_email)

    return {'access_token': access_token}, 200


@user_bp.route('/user', methods=['GET'])
@jwt_required()
def get_current_user():
    user_email = get_jwt_identity()
    
    user_data = redis_client.get(f"user:{user_email}")

    if user_data:
        user_data = json.loads(user_data)
    else:
        user = UserModel.objects(user_email=user_email).first()
        if not user:
            return {'message': 'User not found'}, 404

        user_data = {
            'user_id': user.user_id,
            'user_name': user.user_name,
            'user_email': user.user_email
        }

        # Serialize user data
        user_data = serialize_object_id(user_data)
        redis_client.set(f"user:{user_email}", json.dumps(user_data))

    return {'user': user_data}, 200


@user_bp.route('/user', methods=['PUT'])
@jwt_required()
def update_user():
    user_email = get_jwt_identity()
    user = UserModel.objects(user_email=user_email).first()

    if not user:
        return {'message': 'User not found'}, 404

    data = request.get_json()

    if 'user_name' in data:
        user.user_name = data['user_name']
    
    if 'user_password' in data:
        user.user_password = generate_password_hash(data['user_password'], method='sha256')
    
    user.save()

    user_data = serialize_object_id(user.to_mongo().to_dict())
    redis_client.set(f"user:{user_email}", json.dumps(user_data))

    return {'message': 'User updated successfully'}, 200


@user_bp.route('/user', methods=['DELETE'])
@jwt_required()
def delete_user():
    user_email = get_jwt_identity()
    user = UserModel.objects(user_email=user_email).first()

    if not user:
        return {'message': 'User not found'}, 404

    user.delete()
    redis_client.delete(f"user:{user_email}")

    return {'message': 'User deleted successfully'}, 200
