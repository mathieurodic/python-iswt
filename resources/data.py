import flask
from flask.views import MethodView

from common.exceptions import InvalidInputError

from models.irradiance import Irradiance


class DataResource(MethodView):

    def get(self):
        for key in ('lat', 'lng'):
            if key not in flask.request.args:
                raise InvalidInputError('Missing parameter: %s' % (key, ))
        result = Irradiance(
            latitude = flask.request.args.get('lat'),
            longitude = flask.request.args.get('lng'),
        ).compute()
        return {
            'result': result,
        }
