from mongoengine import Document, StringField, IntField, EmailField, ListField, ReferenceField

class UserModel(Document):
    user_id = IntField(required=True, unique=True)
    user_name = StringField(required=True)
    user_email = EmailField(required=True, unique=True)
    user_password = StringField(required=True)
    
    # Se você quiser que o MongoDB armazene uma lista de IDs de tarefas associadas ao usuário
    user_assignments = ListField(ReferenceField('AssignmentModel'))
    
    meta = {'collection': 'users'}  # Definindo a coleção explicitamente