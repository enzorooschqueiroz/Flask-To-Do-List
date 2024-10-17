from mongoengine import Document, StringField, DateTimeField, ReferenceField
from .user_model import UserModel
import uuid


class AssignmentModel(Document):
    assignment_id = StringField(required=True, default=lambda: str(uuid.uuid4()), unique=True)
    assignment_title = StringField(required=True)
    assignment_description = StringField(required=True)
    assignment_status = StringField(required=True, max_length=10)
    assignment_due_date = DateTimeField(required=True)

    user_id = ReferenceField(UserModel, required=True)

    meta = {'collection': 'assignments'}
