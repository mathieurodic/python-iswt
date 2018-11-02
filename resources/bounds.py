from flask.views import MethodView

import common.config


class BoundsResource(MethodView):

    def get(self):
        """ Returns authorized bounds for data query

            ---

            tags:
                - bounds

            response:
                200:
                    description: everything went fine
                    schema:
                        title: data
                        properties:
                            result:
                                type: number

        """
        return common.config.get('irradiance', 'frame')
