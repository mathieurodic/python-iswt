from common.exceptions import InvalidInputError, ForbiddenError
import common.config


class Irradiance(object):

    def __init__(self, latitude, longitude):
        # check if values are floating-point
        try:
            self.latitude = float(latitude)
            self.longitude = float(longitude)
        except ValueError:
            raise InvalidInputError('Both latitude and longitude should be expressed as floating point values.')
        # check if values are within expected boundaries
        config = common.config.get('irradiance', 'frame')
        for key in ('longitude', 'latitude'):
            if not config[key]['min'] <= getattr(self, key) <= config[key]['max']:
                raise ForbiddenError('Value for {key} should be comprised between {min} and {max}'.format(
                    key=key,
                    **config['latitude']
                ))

    def compute(self):
        return 2000.0 - 900.0 * (self.latitude - 41.0) / (51.5 - 41.0)
