from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user_model import UserModel

user_bp = Blueprint('users', __name__)

@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    # Verifica se o email já está em uso
    if UserModel.objects(user_email=data['user_email']).first():
        return {'message': 'User already exists'}, 400

    hashed_password = generate_password_hash(data['user_password'], method='sha256')

    new_user = UserModel(
        user_name=data['user_name'],
        user_email=data['user_email'],
        user_password=hashed_password
    )
    
    new_user.save()

    return {'message': 'User created successfully'}, 201


@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = UserModel.objects(user_email=data['user_email']).first()

    if not user or not check_password_hash(user.user_password, data['user_password']):
        return {'message': 'Invalid credentials'}, 401

    # Gerando o JWT token
    access_token = create_access_token(identity=user.user_email)

    
    return {'access_token': access_token}, 200

@user_bp.route('/user', methods=['GET'])
@jwt_required()
def get_current_user():
    user_email = get_jwt_identity()
    user = UserModel.objects(user_email=user_email).first()

    if not user:
        return {'message': 'User not found'}, 404

    user_data = {
        'user_id': user.user_id,
        'user_name': user.user_name,
        'user_email': user.user_email
    }

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

    return {'message': 'User updated successfully'}, 200

@user_bp.route('/user', methods=['DELETE'])
@jwt_required()
def delete_user():
    user_email = get_jwt_identity()
    user = UserModel.objects(user_email=user_email).first()

    if not user:
        return {'message': 'User not found'}, 404

    user.delete()

    return {'message': 'User deleted successfully'}, 200