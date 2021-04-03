from flask_restful import Resource


class ApiStatusAPI(Resource):
    def get(self):
        return 'ok'
