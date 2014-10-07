# coding: utf-8
"""
sentry_zabbix.forms
"""
from django import forms

import socket


class ZabbixOptionsForm(forms.Form):
    server_host = forms.CharField(
        max_length=255,
        initial='127.0.0.1',
        help_text='Zabbix host (for example: "localhost")'
    )
    server_port = forms.IntegerField(
        max_value=65535,
        initial='10051',
        help_text='Zabbix port (for example: "10051")'
    )
    prefix = forms.CharField(
        max_length=255,
        initial='sentry',
        help_text='Prefix for Sentry metrics in Zabbix (for example: "sentry")'
    )
    hostname = forms.CharField(
        max_length=255,
        initial=socket.gethostname(),
        help_text='Host name to send to zabbix (for example "%s")' % socket.gethostname(),
    )
