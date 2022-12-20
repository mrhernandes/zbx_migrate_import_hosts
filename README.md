# About
This script migrates only hosts whithout groups and their information to another remote zabbix.

The hosts properties are populated into host description(templates,groups,status)

## Requirements
<b>python3</b>

<b>zabbix-api</b>

https://pypi.org/project/zabbix-api/


## Parameters
To use this script, uncomment the following parameters:

<b>zbxsourceurl</b>:  zabbix url source

<b>zbxsourceuser</b>: zabbix user source

<b>zbxsourcepass</b>: zabbix password source

<b>zbxdesturl</b>: zabbix url destination

<b>zbxdestuser</b>: zabbix user destination

<b>zbxdestpass</b>: zabbix password destination

<b>zbxdestgroup</b>: Group to store hosts into zabbix destination

<b>timeout</b>: Maximum time and duration of the request, value in seconds

## Commands
<b>python3 zbx_import_hosts.py</b>
