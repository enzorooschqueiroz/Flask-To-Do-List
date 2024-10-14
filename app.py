from flask import Flask
from flask_restful import Resource, Api
from flask_mongoengine import MongoEngine


app = Flask(__name__)
api = Api(app)
db = MongoEngine(app)


app.config['MONGODB_SETTING'] = {
    "db": "assignments",
    "host": "mongodb",
    "port": 27017,
    "user": "admin",
    "password": "admin"  # Inserir credenciais do MongoDB aqui
}


class AssignmentModel(db.Document):
    assignment_id = db.IntegerField(required=True, unique=True)
    assignment_title = db.StringField(required=True, unique=False)
    assignment_description = db.StringField(required=True, unique=False)
    assignment_status = db.StringField(required=True, max_length=10)
    assignment_due_date = db.DateTimeField(required=True)

class UserModel(db.Document):
    user_id = db.IntegerField(required=True, unique=True)
    user_name = db.StringField(required=True, unique=False)
    user_email = db.EmailField(required=True, unique=True)
    user_password = db.StringField(required=True, unique=False)
    


class Assignments(Resource):
    def get(self):
        return {'message': "assignment"}


class Assignment(Resource):
    def post(self):
        return {'message': "assignment created"}

    def get(self, asssingment_id):
        return {'message': "assignment 1"}


api.add_resource(Assignments, '/assignments')
api.add_resource(Assignment, '/assignment', 'assignment/<int:assignment_id>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
