from flask import current_app
from flask_marshmallow import Marshmallow
from marshmallow import fields, validate, pre_load

ma = Marshmallow()


class CiteSchema(ma.Schema):
    id = fields.Integer()
    text = fields.String()


class CountdownResultSchema(ma.Schema):
    dateformat = '%Y-%m-%dT%H:%M:%S.%f+00:00'
    id = fields.Integer()
    start_date = fields.DateTime(attribute='start_date', data_key='startDate', format=dateformat)
    finish_date = fields.DateTime(attribute='finish_date', data_key='finishDate', format=dateformat)
    success = fields.Boolean()

    @pre_load
    def fix_date_format(self, in_data, **kwargs):
        current_app.logger.info(in_data)
        if in_data['startDate'].endswith('Z'):
            in_data['startDate'] = in_data['startDate'].replace('Z', '+00:00')
        if in_data['finishDate'].endswith('Z'):
            in_data['finishDate'] = in_data['finishDate'].replace('Z', '+00:00')
        return in_data



class CountdownResultsWithAdditionalDataSchema(ma.Schema):
    totalNumber = fields.Integer()
    data = fields.Nested(CountdownResultSchema, many=True)


class CountdownResultsSorter(ma.Schema):
    property_name = fields.String(attribute='property_name', data_key='propertyName', required=True,
                                  validate=validate.OneOf(['startDate', 'finishDate', 'success']))
    order = fields.String(required=True, validate=validate.OneOf(['ASC', 'DESC']))


class CountdownResultsFilter(ma.Schema):
    countdown_status = fields.String(attribute='countdown_status', data_key='countdownStatus',
                                     validate=validate.OneOf(['all', 'success', 'failure']))
    start_date = fields.DateTime(attribute='start_date', data_key='startDate', required=False, default=None,
                                 allow_none=True, format='iso')
    finish_date = fields.DateTime(attribute='finish_date', data_key='finishDate', required=False, default=None,
                                  allow_none=True, format='iso')


class CountdownResultsQuerySchema(ma.Schema):
    filter = fields.Nested(CountdownResultsFilter, many=False)
    page = fields.Integer(default=1, data_key='page')
    page_size = fields.Integer(default=10, data_key='pageSize')
    sorters = fields.Nested(CountdownResultsSorter, many=True, required=False)
