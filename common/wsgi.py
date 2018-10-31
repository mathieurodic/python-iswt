""" This module is just there to provide a direct access to the `app` for WSGI servers.
"""


# the Flask application itself

import common.app

application = common.app.create()
