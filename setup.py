#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = [
    'sentry>=8.0.0',
    'zbxsend',
]

f = open('README.rst')
readme = f.read()
f.close()

setup(
    name='sentry-zabbix',
    version='0.0.16',
    author='Sabin Iacob',
    author_email='iacobs+pypi@gmail.com',
    url='http://github.com/m0n5t3r/sentry-zabbix',
    description='A Sentry extension which send errors stats to Zabbix',
    long_description=readme,
    license='WTFPL',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=install_requires,
    entry_points={
        'sentry.plugins': [
            'sentry_zabbix = sentry_zabbix.plugin:ZabbixPlugin'
        ],
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Topic :: Software Development'
    ],
    keywords='sentry zabbix',
)
