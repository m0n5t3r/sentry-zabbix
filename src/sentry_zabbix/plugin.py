# coding: utf-8
"""
sentry_zabbix.plugin
"""

import socket
import logging
import sentry_zabbix
import time

from sentry.plugins import Plugin
from zbxsend import Metric, send_to_zabbix

log = logging.getLogger('sentry')

from sentry_zabbix.forms import ZabbixOptionsForm


class ZabbixPlugin(Plugin):
    """
    Sentry plugin to send error counts to Zabbix.
    """
    author = 'Sabin Iacob'
    author_url = 'https://github.com/m0n5t3r/sentry-zabbix'
    version = sentry_zabbix.VERSION
    description = 'Send error counts to Zabbix.'
    slug = 'zabbix'
    title = 'Zabbix'
    conf_key = slug
    conf_title = title
    resource_links = [
        ('Source', 'https://github.com/m0n5t3r/sentry-zabbix'),
        ('Bug Tracker', 'https://github.com/m0n5t3r/sentry-zabbix/issues'),
        ('README', 'https://github.com/m0n5t3r/sentry-zabbix/blob/master/README.rst'),
    ]
    project_conf_form = ZabbixOptionsForm

    def is_configured(self, project, **kwargs):
        """
        Check if plugin is configured.
        """
        params = self.get_option
        return bool(params('server_host', project) and params('server_port', project))

    def post_process(self, group, event, is_new, is_sample, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return

        now = int(time.time())
        host = self.get_option('server_host', group.project)
        port = self.get_option('server_port', group.project)
        prefix = self.get_option('prefix', group.project)
        prefix = '%s.%%s[%s]' % (prefix, group.project.slug)

        hostname = self.get_option('hostname', group.project) or socket.gethostname()

        metrics = []

        metrics.append(
            Metric(hostname, prefix % 'event', 1, now)
        )

        log.info('will send %s to zabbix', prefix % 'event')

        send_to_zabbix(metrics, host, port)
