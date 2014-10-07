# coding: utf-8
"""
sentry_zabbix
"""
try:
    VERSION = __import__('pkg_resources').get_distribution(__name__).version
except Exception, e:
    VERSION = 'unknown'
