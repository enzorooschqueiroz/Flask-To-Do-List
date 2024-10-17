from mongoengine import Document, StringField, EmailField, ListField, ReferenceField
import uuid


class UserModel(Document):
    user_id = StringField(required=True, default=lambda: str(uuid.uuid4()), unique=True)
    user_name = StringField(required=True)
    user_email = EmailField(required=True, unique=True)
    user_password = StringField(required=True)

    user_assignments = ListField(ReferenceField('AssignmentModel'))

    meta = {'collection': 'users'}
