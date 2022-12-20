[About]
This script migrates hosts and their information to another remote zabbix.

[Parameters]
To use this script, uncomment the following parameters:

zbxsourceurl:  zabbix url source 
zbxsourceuser: zabbix user source
zbxsourcepass: zabbix password source

zbxdesturl: zabbix url destination
zbxdestuser: zabbix user destination
zbxdestpass: zabbix password destination

zbxdestgroup: Group to Store hosts into zabbix destination

timeout: Maximum time and duration of the request, value in seconds

[Commands]
python3 zbx_import_hosts.py
