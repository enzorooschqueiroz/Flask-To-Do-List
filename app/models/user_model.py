from mongoengine import Document, StringField, IntField, EmailField, ListField, ReferenceField
import uuid

class UserModel(Document):
    user_id = StringField(required=True, default=lambda: str(uuid.uuid4()), unique=True)
    user_name = StringField(required=True)
    user_email = EmailField(required=True, unique=True)
    user_password = StringField(required=True)
    
    # Se você quiser que o MongoDB armazene uma lista de IDs de tarefas associadas ao usuário
    user_assignments = ListField(ReferenceField('AssignmentModel'))
    
    meta = {'collection': 'users'}  # Definindo a coleção explicitamente