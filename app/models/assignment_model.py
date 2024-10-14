from mongoengine import Document, StringField, IntField, DateTimeField, ReferenceField
from .user_model import UserModel

class AssignmentModel(Document):
    assignment_id = IntField(required=True, unique=True)
    assignment_title = StringField(required=True)
    assignment_description = StringField(required=True)
    assignment_status = StringField(required=True, max_length=10)
    assignment_due_date = DateTimeField(required=True)
    
    user_id = ReferenceField(UserModel, required=True)

    meta = {'collection': 'assignments'}  
