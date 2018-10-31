import logging.config

import common.config


def configure():
    """ Configure logging, according to what has been defined in `etc/logging.yaml`.
    """
    logging_config = common.config.get('logging')
    logging.config.dictConfig(logging_config)
