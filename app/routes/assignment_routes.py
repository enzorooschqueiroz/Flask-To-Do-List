from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.assignment_model import AssignmentModel
from app.models.user_model import UserModel
from datetime import datetime
from bson import ObjectId

assignment_bp = Blueprint('assignments', __name__)


def serialize_object_id(data):
    if isinstance(data, dict):
        return {key: serialize_object_id(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [serialize_object_id(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    return data


@assignment_bp.route('/assignment', methods=['POST'])
@jwt_required()
def create_assignment():
    current_user_email = get_jwt_identity()
    user = UserModel.objects(user_email=current_user_email).first()

    if not user:
        return {'message': 'User not found'}, 404

    data = request.get_json()
    new_assignment = AssignmentModel(
        assignment_title=data['assignment_title'],
        assignment_description=data['assignment_description'],
        assignment_status=data['assignment_status'],
        assignment_due_date=datetime.strptime(data['assignment_due_date'], '%Y-%m-%d'),
        user_id=user
    )

    new_assignment.save()

    assignment_data = new_assignment.to_mongo().to_dict()
    assignment_data = serialize_object_id(assignment_data)

    return {'message': 'Assignment created', 'assignment': assignment_data}, 201


@assignment_bp.route('/assignments', methods=['GET'])
@jwt_required()
def get_assignments():
    current_user_email = get_jwt_identity()
    user = UserModel.objects(user_email=current_user_email).first()

    if not user:
        return {'message': 'User not found'}, 404

    assignments_list = []
    for assignment in AssignmentModel.objects(user_id=user):
        assignment_data = {
            'assignment_id': str(assignment.assignment_id),
            'assignment_title': assignment.assignment_title,
            'assignment_description': assignment.assignment_description,
            'assignment_status': assignment.assignment_status,
            'assignment_due_date': assignment.assignment_due_date.strftime('%Y-%m-%d')
        }
        assignments_list.append(assignment_data)

    return {'assignments': assignments_list}, 200


@assignment_bp.route('/assignment/<assignment_id>', methods=['DELETE'])
@jwt_required()
def delete_assignment(assignment_id):
    current_user_email = get_jwt_identity()
    user = UserModel.objects(user_email=current_user_email).first()

    if not user:
        return {'message': 'User not found'}, 404

    assignment = AssignmentModel.objects(assignment_id=assignment_id, user_id=user).first()

    if not assignment:
        return {'message': 'Assignment not found'}, 404

    assignment.delete()

    user.user_assignments = [a for a in user.user_assignments if a.assignment_id != assignment.assignment_id]
    user.save()

    return {'message': 'Assignment deleted successfully'}, 200


@assignment_bp.route('/assignment/<assignment_id>', methods=['PUT'])
@jwt_required()
def update_assignment(assignment_id):
    current_user_email = get_jwt_identity()
    user = UserModel.objects(user_email=current_user_email).first()

    if not user:
        return {'message': 'User not found'}, 404

    assignment = AssignmentModel.objects(assignment_id=assignment_id, user_id=user).first()

    if not assignment:
        return {'message': 'Assignment not found'}, 404

    data = request.get_json()

    if 'assignment_title' in data:
        assignment.assignment_title = data['assignment_title']
    if 'assignment_description' in data:
        assignment.assignment_description = data['assignment_description']
    if 'assignment_status' in data:
        assignment.assignment_status = data['assignment_status']
    if 'assignment_due_date' in data:
        assignment.assignment_due_date = datetime.strptime(data['assignment_due_date'], '%Y-%m-%d')

    assignment.save()

    return {'message': 'Assignment updated successfully'}, 200


@assignment_bp.route('/assignment/<assignment_id>', methods=['GET'])
@jwt_required()
def get_assignment_by_id(assignment_id):
    current_user_email = get_jwt_identity()
    user = UserModel.objects(user_email=current_user_email).first()

    if not user:
        return {'message': 'User not found'}, 404

    assignment = AssignmentModel.objects(assignment_id=assignment_id, user_id=user).first()

    if not assignment:
        return {'message': 'Assignment not found'}, 404

    assignment_data = {
        'assignment_id': str(assignment.assignment_id),
        'assignment_title': assignment.assignment_title,
        'assignment_description': assignment.assignment_description,
        'assignment_status': assignment.assignment_status,
        'assignment_due_date': assignment.assignment_due_date.strftime('%Y-%m-%d')
    }

    return {'assignment': assignment_data}, 200
