from random import randint, choice

from flask_restful import Resource

from app import models
from app.api.schemas import CiteSchema


class CiteAPI(Resource):

    def __init__(self):
        self.schema = CiteSchema(many=False)


    # @login_required this annotation will work
    def get(self, id=None):
        cites = models.Cite.query.all()
        if len(cites) == 0:
            return 'There is no cite in the db'
        else:
            cite = choice(cites)
            return self.schema.jsonify(cite)
