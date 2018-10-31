import flask
import flask.logging
import flask_restful
import flasgger
import logging

import common.config
import common.logging
import common.decorators


common.logging.configure()


def create():
    """ Method to get the Flask application object.

        Returns:
            flask.Flask: The Flask application, as configured in `etc/rest.yaml`.

        Raises:
            ImportError: One of the resource classes of the `urls` key in the
                `mappings` section of the `etc/rest.yaml` configuration file
                could not be retrieved.
    """

    # inititialize application
    app = flask.Flask(__name__)
    app.debug = common.config.get('rest', 'debug')
    if app.debug:
        print('(Re)loaded application...')

    # inititialize REST
    api = flask_restful.Api(app) # see https://github.com/flask-restful/flask-restful/issues/116

    # iterate over mappings and integrate them into the Flask application
    rest_mappings = common.config.get('rest', 'mappings')
    for m, mapping in enumerate(rest_mappings):
        url = mapping['url']
        resource_fullpath = mapping['resource']
        module_name_lastindex = resource_fullpath.rfind('.')
        # retrieve module
        module_path = resource_fullpath[:module_name_lastindex]
        module = __import__(module_path, fromlist=[''])
        # retrieve resource
        resource_path = resource_fullpath[module_name_lastindex + 1:]
        try:
            resource = getattr(module, resource_path)
        except AttributeError:
            raise ImportError('No resource named `%s` in `%s`, check your configuration file' % (
                resource_path,
                module_path,
            ))
        # add decorator
        resource.decorators = [common.decorators.ResourceDecorator] + list(getattr(resource, 'decorators', []))
        # associate resource with URL
        resource_name = '%d_%s' % (m, resource.__name__)
        api.add_resource(resource, url, endpoint=resource_name)

    # API documentation
    swagger_config = flasgger.Swagger.DEFAULT_CONFIG.copy()
    for index, header in enumerate(swagger_config['headers']):
        if header[0] == 'Access-Control-Allow-Methods':
            swagger_config['headers'][index] = ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS, PATCH')
    swagger_config['specs'][0].update(
        version = common.config.get('rest', 'service_version'),
        title = 'API ' + (common.config.get('rest', 'service_name') or ''),
        description = 'Documentation for the access points on API ' + (common.config.get('rest', 'service_name') or ''),
    )
    flasgger.Swagger(app, config = swagger_config)

    # that's all, folks!
    return app
