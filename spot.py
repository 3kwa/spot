import json

import yaml


class Service:
    """ Base class for Dotcloud services

    Subclasses should define a method _server(self) for the property server
    to call which return a connection to the service.
    """
    @property
    def server(self):
        return self._server()

class Redis(Service):
    """ Common development parameters for Redis server """
    host = u'localhost'
    port = 6379
    password = None

    def _server(self):
        import redis
        return redis.StrictRedis(host=self.host,
                                 port=self.port,
                                 password=self.password)

class Mongodb(Service):
    """ Common development parameters for MongoDB server """
    url = None

    def _server(self):
        import pymongo
        return pymongo.Connection(self.url)


class Dotcloud(object):
    """ Developement/Dotcloud service parameters 'abstraction' layer

    >>> Dotcloud.dotcloud_yaml = 'fixtures/dotcloud.yml'
    >>> dotcloud = Dotcloud()
    >>> dotcloud.cache.port
    6379
    """

    dotcloud_yaml = 'dotcloud.yml'
    environment_json = '/home/dotcloud/environment.json'

    def __init__(self):
        self.dotcloud = {}
        self._load()

    def _load(self):
        """ Load the service parameters """
        try:
            # are we on dotcloud?
            with open(self.environment_json) as f:
                self._json(f)
        except IOError:
            # are we on development
            with open(self.dotcloud_yaml) as f:
                self._yaml(f)

    def _yaml(self, file_):
        """
        >>> import StringIO
        >>> f = StringIO.StringIO(yaml.dump({'cache': {'type': 'redis'}}))
        >>> env = Dotcloud()
        >>> env._yaml(f)
        >>> env.cache.host
        u'localhost'
        """
        for service_name, service_property in yaml.load(file_).items():
            service_type = service_property['type']
            try:
                self.dotcloud[service_name] = globals()[service_type.capitalize()]()
            except KeyError:
                # unknown service_type
                pass

    def _json(self, file_):
        """
        >>> import StringIO
        >>> f = StringIO.StringIO(
        ...     json.dumps({'DOTCLOUD_CACHE_REDIS_HOST': 'dotcloud',
        ...                 'DOTCLOUD_CACHE_REDIS_PORT': '1234',
        ...                 'DOTCLOUD_CACHE_REDIS_PASSWORD': 'secret' }))
        >>> env = Dotcloud()
        >>> env._json(f)
        >>> env.cache.host
        u'dotcloud'
        >>> env.cache.port
        1234
        >>> env.cache.password
        u'secret'
        >>> f = StringIO.StringIO(fixture)
        >>> env._json(f)
        >>> env.mongo.url
        u'mongodb://root:PASSWORD@albinos-3kwa-mongo-0.dotcloud.com:28162'
        """
        environment_json = json.load(file_)
        services  = {}
        for key,service_value in environment_json.items():
            try:
                ignore, service_name, service_type, service_var = key.lower().split('_')
            except ValueError:
                # key not service related
                continue
            # dynamically instantiating a class based on service_type
            try:
                self.dotcloud[service_name] = globals()[service_type.capitalize()]()
            except KeyError:
                # no service class for service_type
                continue
            man = services.setdefault(service_name, {})
            man[service_var] = service_value

        for service_name, service_property in services.items():
            service = self.dotcloud[service_name]
            for service_var, service_value in service_property.items():
                try:
                    man = getattr(service, service_var)
                except AttributeError:
                    # exposed in environment.json but not in service definition
                    continue
                else:
                    # casting the type to the service definition type
                    if man is not None:
                        service_value = type(man)(service_value)
                setattr(service, service_var, service_value)

    def __getattr__(self, name):
        return self.dotcloud[name]

fixture = """{
"DOTCLOUD_WWW_HTTP_URL": "http://albinos-3kwa.dotcloud.com/",
"DOTCLOUD_CACHE_REDIS_URL": "redis://root:PASSWORD@albinos-3kwa.dotcloud.com:28088",
"DOTCLOUD_WWW_SSH_PORT": "28073",
"DOTCLOUD_CACHE_SSH_URL": "ssh://redis@albinos-3kwa.dotcloud.com:28086",
"DOTCLOUD_WWW_SSH_URL": "ssh://dotcloud@albinos-3kwa.dotcloud.com:28073",
"DOTCLOUD_MONGO_SSH_HOST": "albinos-3kwa-mongo-0.dotcloud.com",
"DOTCLOUD_WWW_SSH_HOST": "albinos-3kwa.dotcloud.com",
"DOTCLOUD_CACHE_SSH_HOST": "albinos-3kwa.dotcloud.com",
"DOTCLOUD_PROJECT": "albinos",
"DOTCLOUD_SERVICE_NAME": "www",
"DOTCLOUD_MONGO_SSH_PORT": "28161",
"DOTCLOUD_CACHE_REDIS_PORT": "28088",
"PORT_SSH": 22,
"DOTCLOUD_WWW_HTTP_HOST": "albinos-3kwa.dotcloud.com",
"PORT_HTTP": 80,
"DOTCLOUD_ENVIRONMENT": "default",
"DOTCLOUD_MONGO_MONGODB_PORT": "28162",
"DOTCLOUD_MONGO_SSH_URL": "ssh://mongodb@albinos-3kwa-mongo-0.dotcloud.com:28161",
"DOTCLOUD_CACHE_REDIS_HOST": "albinos-3kwa.dotcloud.com",
"DOTCLOUD_MONGO_MONGODB_PASSWORD": "PASSWORD",
"DOTCLOUD_MONGO_MONGODB_LOGIN": "root",
"DOTCLOUD_MONGO_MONGODB_URL": "mongodb://root:PASSWORD@albinos-3kwa-mongo-0.dotcloud.com:28162",
"DOTCLOUD_CACHE_REDIS_LOGIN": "root",
"DOTCLOUD_CACHE_REDIS_PASSWORD": "PASSWORD",
"DOTCLOUD_SERVICE_ID": "0",
"DOTCLOUD_MONGO_MONGODB_HOST": "albinos-3kwa-mongo-0.dotcloud.com",
"DOTCLOUD_CACHE_SSH_PORT": "28086"
}"""
