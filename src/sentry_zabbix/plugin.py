# coding: utf-8
"""
sentry_zabbix.plugin
"""

import socket
from sentry.plugins import Plugin
from zbxsend import Metric, send_to_zabbix

import sentry_zabbix
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
        return bool(params('host', project) and params('port', project))

    def post_process(self, group, event, is_new, is_sample, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return

        host = self.get_option('host', group.project)
        port = self.get_option('port', group.project)
        prefix = self.get_option('prefix', group.project)
        prefix = '%s.%%s[%s]' % (prefix, group.project.slug)

        hostname = socket.gethostname()

        metrics = []

        metrics.append(
            Metric(hostname, prefix % 'count', group.event_set.count())
        )

        metrics.append(
            Metric(hostname, prefix % 'level', group.get_level_display())
        )

        send_to_zabbix(metrics, host, port)
