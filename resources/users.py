from flask_restful import Resource, Api

class Users(Resource):

    def post(self):
        return {'status': 'success'}

    def get(self):
        return {'user': '1'}
