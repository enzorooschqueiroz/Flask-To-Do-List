from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.assignment_model import AssignmentModel
from app.models.user_model import UserModel
from datetime import datetime

assignment_bp = Blueprint('assignments', __name__)

@assignment_bp.route('/assignment', methods=['POST'])
@jwt_required()
def create_assignment():
    current_user_email = get_jwt_identity()  # Obtendo o usuário autenticado pelo JWT
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

    user.user_assignments.append(new_assignment)
    user.save()

    return {'message': 'Assignment created'}, 201


@assignment_bp.route('/assignments', methods=['GET'])
@jwt_required()
def get_assignments():
    current_user_email = get_jwt_identity()  
    user = UserModel.objects(user_email=current_user_email).first()

    if not user:
        return {'message': 'User not found'}, 404

    # Obtendo todas as tarefas associadas ao usuário autenticado
    assignments = AssignmentModel.objects(user_id=user)
    assignments_list = [{
        'assignment_id': str(a.assignment_id),
        'assignment_title': a.assignment_title,
        'assignment_description': a.assignment_description,
        'assignment_status': a.assignment_status,
        'assignment_due_date': a.assignment_due_date.strftime('%Y-%m-%d')
    } for a in assignments]

    return {'assignments': assignments_list}, 200
