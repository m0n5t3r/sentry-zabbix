# coding: utf-8
"""
sentry_zabbix
"""
from __future__ import absolute_import

try:
    VERSION = __import__('pkg_resources').get_distribution(__name__).version
except Exception, e:
    VERSION = 'unknown'

from sentry.plugins import register
from .plugin import ZabbixPlugin

# register(ZabbixPlugin)
