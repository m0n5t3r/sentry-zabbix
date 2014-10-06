sentry-zabbix
=============

An extension for Sentry to send errors metrics to Zabbix; shamelessly based on (sentry-statsd)[https://github.com/dreadatour/sentry-statsd].

Install
-------

Install the package with ``pip``::

    pip install sentry-zabbix


Configuration
-------------

Go to your project's configuration page (Projects -> [Project]) and select the
"Zabbix" tab. Enter the Zabbix host, port and prefix for metrics:

.. image:: https://github.com/m0n5t3r/sentry-zabbix/raw/master/docs/images/options.png


After installing and configuring, make sure to restart sentry-worker for the
changes to take into effect.
