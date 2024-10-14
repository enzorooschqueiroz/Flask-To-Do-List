from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


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
