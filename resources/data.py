import flask
from flask.views import MethodView

from common.exceptions import InvalidInputError

from models.irradiance import Irradiance


class DataResource(MethodView):

    def get(self):
        """ Compute yearly irradiance at a given point

            ---

            tags:
                - data

            parameters:
                - name: lng
                  description: longitude of the given point
                  in: query
                  type: double
                  required: true
                - name: lat
                  description: latitude of the given point
                  in: query
                  type: double
                  required: true

            responses:
                200:
                    description: everything went fine
                    schema:
                        title: data
                        properties:
                            result:
                                type: number
                400:
                    description: either one of the parameters is missing, or is not a proper floating point numbers
                403:
                    description: the coordinates of the point are out of the defined boundaries
                500:
                    description: oops, this means there are some bugs left... please report!

        """
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
