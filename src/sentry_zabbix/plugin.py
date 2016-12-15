# coding: utf-8
"""
sentry_zabbix.plugin
"""

import socket
import sentry_zabbix
import time

from datetime import timedelta
from django.utils import timezone
from django.utils.log import getLogger

from sentry.plugins.bases.notify import NotificationPlugin
from sentry.constants import STATUS_UNRESOLVED

from sentry.models import Activity

from zbxsend import Metric, send_to_zabbix

from sentry_zabbix.forms import ZabbixOptionsForm

log = getLogger()


class ZabbixPlugin(NotificationPlugin):
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
        port = int(self.get_option('server_port', group.project))
        prefix = self.get_option('prefix', group.project)
        hostname = self.get_option('hostname', group.project) or socket.gethostname()
        resolve_age = group.project.get_option('sentry:resolve_age', None)

        now = int(time.time())
        template = '%s.%%s[%s]' % (prefix, group.project.slug)

        level = group.get_level_display()
        label = template % level

        groups = group.project.group_set.filter(status=STATUS_UNRESOLVED)

        if resolve_age:
            oldest = timezone.now() - timedelta(hours=int(resolve_age))
            groups = groups.filter(last_seen__gt=oldest)

        num_errors = groups.filter(level=group.level).count()

        metric = Metric(hostname, label, num_errors, now)

        log.info('will send %s=%s to zabbix', label, num_errors)

        send_to_zabbix([metric], host, port)

    def notify_users(self, *args, **kwargs):
        pass

    def notify_about_activity(self, activity):
        if activity.type not in (Activity.SET_RESOLVED, Activity.SET_UNRESOLVED):
            return

        log.info('got activity type %s for group %s', activity.type, activity.group)
        self.post_process(group=activity.group, event=None, is_new=False, is_sample=False)
