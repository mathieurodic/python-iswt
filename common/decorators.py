import common.exceptions
import common.logging
import common.generators

import sys
import traceback
import time
import json
import flask
import flask_restful
import werkzeug.exceptions

import logging
common.logging.configure()


class ResourceDecorator(object):

    _logger = logging.getLogger('http')
    _caught_exceptions = (
        common.exceptions.InvalidInputError,
        common.exceptions.ForbiddenError,
        common.exceptions.NotFoundError,
        common.exceptions.ConflictError,
        common.exceptions.DuplicateError,
        common.exceptions.ServiceError,
    )

    def __init__(self, decorated_method):
        self._decorated_method = decorated_method

    @staticmethod
    def generate_meta(start_time, result):
        """ Generate metadata to be appended to the JSON data
        """
        return {
            'service': common.config.get('rest', 'service_name'),
            'version': common.config.get('rest', 'service_version'),
            'path': flask.request.path,
            'method': flask.request.method,
            'parameters': {
                'headers': dict(flask.request.headers),
                'form': dict(flask.request.form or {}),
                'args': dict(flask.request.args or {}),
                'json': flask.request.json,
            },
            'timestamp': {
                'start': start_time,
                'end': time.time(),
            },
            'response': {
                'code': result[1],
            }
        }

    def __call__(self, *args, **kwargs):
        # remember when we started
        start_time = time.time()
        # try to execute the decorated method
        try:
            result = self._decorated_method(*args, **kwargs)
        except werkzeug.exceptions.HTTPException as error:
            if hasattr(error, 'data'):
                data = error.data
            else:
                data = ''
            result = data, error.code, error.get_headers()
        except self._caught_exceptions as error:
            result = {
                'message': error.args[0],
                'type': error.__class__.__name__
            }, error.http_code, {}
        except Exception as error:
            exec_info = sys.exc_info()
            result = {
                'type': error.__class__.__module__ + '.' + error.__class__.__name__,
                'message': str(error),
                'traceback': traceback.format_exception(*exec_info),
            }, 500, {}
        # format result if necessary
        if not isinstance(result, tuple):
            result = result, 200, {}
        if result[1] == 204:
            result = {}, 200, {}
        # logging
        log_level = {
            4: logging.WARNING,
            5: logging.ERROR,
        }.get(result[1]//100, logging.DEBUG)
        request_identifier = common.generators.wordlike_identifier(7)
        self._logger.log(log_level, '%s: %s %s\n\t%s\n\t%s' % (
            request_identifier,
            flask.request.method,
            flask.request.url,
            json.dumps(dict(flask.request.headers), indent=4).replace('\n', '\n\t'),
            json.dumps(flask.request.json, indent=4).replace('\n', '\n\t'),
        ))
        try:
            debugvalue = json.dumps(result[0], indent=4).replace('\n', '\n\t')
        except:
            debugvalue = repr(result[0])
        self._logger.log(log_level, '%s:%s: \n\t%s' % (
            request_identifier,
            result[1],
            debugvalue,
        ))
        # add meta parameter and return corresponding result
        try:
            if common.config.get('rest', 'debug') and isinstance(result[0], dict):
                result[0].update(_meta = self.generate_meta(start_time, result))
        except Exception as error:
            try:
                result[0].update(_meta = {
                    'ERROR_WHILE_GENERATING_META': str(error)
                })
            except:
                pass
        return result
