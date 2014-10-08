# coding: utf-8
"""
sentry_zabbix.plugin
"""

import socket
import logging
import sentry_zabbix
import time

from sentry.plugins import Plugin
from sentry.constants import STATUS_UNRESOLVED, STATUS_RESOLVED
from sentry.tasks.post_process import plugin_post_process_group

from zbxsend import Metric, send_to_zabbix

from sentry_zabbix.forms import ZabbixOptionsForm

log = logging.getLogger('root')


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

        host = self.get_option('server_host', group.project)
        port = self.get_option('server_port', group.project)
        prefix = self.get_option('prefix', group.project)
        hostname = self.get_option('hostname', group.project) or socket.gethostname()

        now = int(time.time())
        template = '%s.%%s[%s]' % (prefix, group.project.slug)

        level = group.get_level_display()
        label = template % level
        num_events = group.project.group_set.filter(status=STATUS_UNRESOLVED).count()

        metrics = []

        metrics.append(Metric(hostname, label, num_events, now))
        log.info('will send %s to zabbix', label)

        send_to_zabbix(metrics, host, port)


def _send_to_zabbix(instance, created, **kwargs):
    if instance.status == STATUS_RESOLVED:
        plugin_post_process_group.delay('zabbix', instance)


from sentry.models import Group
from django.db.models.signals import post_save

post_save.connect(_send_to_zabbix, sender=Group)
