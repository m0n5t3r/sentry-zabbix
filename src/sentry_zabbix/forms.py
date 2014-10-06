# coding: utf-8
"""
sentry_zabbix.forms
"""
from django import forms


class ZabbixOptionsForm(forms.Form):
    host = forms.CharField(
        max_length=255,
        initial='127.0.0.1',
        help_text='Zabbix host (for example: "localhost")'
    )
    port = forms.IntegerField(
        max_value=65535,
        initial='10051',
        help_text='Zabbix port (for example: "10051")'
    )
    prefix = forms.CharField(
        max_length=255,
        initial='sentry',
        help_text='Prefix for Sentry metrics in Zabbix (for example: "sentry")'
    )
