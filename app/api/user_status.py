import time

from flask_restful import Resource

from app.auth.views import current_user


class UserStatusAPI(Resource):


    def get(self):
        return current_user.is_authenticated(), 200
