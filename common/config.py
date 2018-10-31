import os
import yaml


_config_cache = {}


def get(config_name, *path):
    """ Get a value from the configuration file.

        Note:
            Instead of reloading configuration files every time this function
            is called, we keep a cache of their parsed contents.

        Arguments:
            config_name (str): path of the configuration file within the `etc`
                directory, without its `.yaml` extension.
            path (List[str]): path to the requested value within the
                configuration file, expressed as a list of keys.

        Returns:
            The corresponding value found in the configuration, or `None` if
            nothing was found.
    """

    # if the result is not cached
    if config_name not in _config_cache:
        # load config from file
        config_filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '../etc/%s.yaml' % (config_name, ),
        )
        config_file = open(config_filename)
        config = yaml.load(config_file)
        _config_cache[config_name] = config

    # iterate to find result
    try:
        result = _config_cache[config_name]
        for iteration in path:
            result = result[iteration]
        return result
    except KeyError:
        return None
