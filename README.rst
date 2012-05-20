==================================
SPOT - DotCloud environment loader
==================================

Why?
====

When working with DotCloud_ you will more than likely have a developement
environment locally that offers the services your application requires which
are specified in the `build file`_.

Locally one very rarely bother changing the parameters of the services from
their defaults settings but on DotCloud_ your application must read the
`environment file`_.

Hence you end up with a fair amount of boilerplate code in your application
which figures out wether it is running locally or on DotCloud_ and instantiates
the services for you to use accordingly.

Not anymore ... if you don't want to ;)

How?
====

Enters SPOT (named after the French earth observation satellite). SPOT knows
wether your code is running locally or on DotCloud_, exposes each service
parameters under the name you gave it in your `build file`_.

For example if your build file contains a python_ service named www and a redis_
service named cache::

    www:
        type: python
    cache:
        type: redis

Then when you instantiate a spot.Dotcloud() object it will expose the cache
services::

    >>> import spot
    >>> dotcloud = spot.Dotcloud()
    >>> isinstance(dotcloud.cache, spot.Redis)
    True

When running locally::

    >>> dotcloud.cache.host
    u'localhost'

But on DotCloud::

    >>> dotcloud.cache.host
    u'SOMETHING.dotcloud.com'

If you have installed the packages allowing Python to handle the services e.g.
redis_ (and hiredis_), the spot.Dotcloud instance also expose a connection to
the server you can use out of the box::

    >>> type(dotcloud.cache.server)
    <class 'redis.client.StrictRedis'>

Next?
=====

At this stage only the Redis_ and MongoDB_ services are managed. I will had more
as I *require* them ... or you can contribute and submit new services definition
via pull request ;)



.. _DotCloud: http://dotcloud.com
.. _redis: http://redis.io
.. _python: http://python.org
.. _build file: http://docs.dotcloud.com/guides/build-file/
.. _environment file: http://docs.dotcloud.com/guides/environment/
.. _redis: http://pypi.python.org/pypi/redis
.. _hiredis: http://pypi.python.org/pypi/hiredis
.. _mongodb: http://www.mongodb.org/
