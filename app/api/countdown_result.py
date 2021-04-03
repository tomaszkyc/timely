from flask import request, current_app
from flask_restful import Resource

from app import models
from app.api.schemas import CountdownResultSchema, CountdownResultsWithAdditionalDataSchema, CountdownResultsQuerySchema
from app.auth.views import current_user, authorized_or_403
from app.models import CountdownResult, db

class CountdownResultAPI(Resource):

    def __init__(self):
        self.schema = CountdownResultSchema(many=True)
        self.get_schema = CountdownResultsWithAdditionalDataSchema(many=False)
        self.query_schema = CountdownResultsQuerySchema()

    @authorized_or_403
    def get(self, id=None):
        filters = self.query_schema.loads(request.args['data'])
        countdown_results, total = models.CountdownResult.find_by_query_parameter(filters, current_user.id)

        response = dict(data=countdown_results, totalNumber=total)
        return self.get_schema.jsonify(response)

    @authorized_or_403
    def post(self, id=None):
        current_app.logger.info("Request data: %s", request.form)
        data = self.schema.loads(request.form['data'])
        if data:
            db_entries = [CountdownResult(entry['start_date'], entry['finish_date'], entry['success'], current_user.id)
                          for entry in data]
            db.session.add_all(db_entries)
            db.session.commit()
            return 'ok', 201

    @authorized_or_403
    def delete(self, id=None):
        current_app.logger.info('Got DELETE REQUEST')
        CountdownResult.delete_all_by_user_id(current_user.id)
        db.session.commit()
        current_app.logger.info('Countdown results has been successfully deleted.')
