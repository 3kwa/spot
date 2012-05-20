==================================
SPOT - DotCloud environment loader
==================================

Why?
====

When working with DotCloud_ you will more than likely have a developement
environment locally that offers the services your application requires which
are specified in the build file.

Locally one very rarely bother changing the default parameter of the services
from their defaults settings but on DotCloud _your application must read the
environement file.

Hence you end up with a fair amount of boilerplate code in your application.
Not anymore!

How?
====

Enters SPOT (named after the French earth observation satellite). SPOT knows
wether your code is running locally or on DotCloud_, exposes each service
parameters under the name you gave it in your build file.

For example if your build file contains a python_ service named www and a redis_
service named cache::

    www:
        type: python
    cache:
        type: redis

Then when you instantiate a spot.Dotcloud() object it will expose the cache
services::

    >>> import spot
    >>> dotcloud = spot.DotCloud()
    >>> isinstance(dotcloud.cache, spot.Redis)
    True



.. _DotCloud: http://dotcloud.com

