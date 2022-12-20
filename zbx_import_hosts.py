#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script migrates hosts and their information to another remote zabbix.
# Created by Hernandes Martins 11/2022
# Reviewd by Rafael Magalhaes 12/2022

# Python Modules
from zabbix_api import ZabbixAPI
import ssl
import configparser

# Read config file config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Read parameters in file config.ini
zbxsourceaurl = config['DefaultConfigSource']['zbxsourceurl']
zbxsourceauser = config['DefaultConfigSource']['zbxsourceuser']
zbxsourceapass = config['DefaultConfigSource']['zbxsourcepass']
zbxdestburl = config['DefaultConfigDest']['zbxdesturl']
zbxdestbuser = config['DefaultConfigDest']['zbxdestuser']
zbxdestbpass = config['DefaultConfigDest']['zbxdestpass']
zbxgrouptomigrate = config['DefaultConfigDest']['zbxdestgroup']
timeout = config['DefaultConfig']['timeout']

# Functions Parameters
def connect_zbx_source():
    zapi = ZabbixAPI(server=zbxsourceaurl,timeout=int(timeout))
    zapi.validate_certs = False
    ssl._create_default_https_context = ssl._create_unverified_context
    zapi.login(zbxsourceauser,zbxsourceapass)
    return zapi

def connect_zbx_dest():
    zapi = ZabbixAPI(server=zbxdestburl,timeout=int(timeout))
    zapi.validate_certs = False
    ssl._create_default_https_context = ssl._create_unverified_context
    zapi.login(zbxdestbuser,zbxdestbpass)
    return zapi

def get_hosts_zbx_source():
    #Getting list of hosts zabbix server source
    zapi = connect_zbx_source()
    hostsA = zapi.host.get({"output": ["name","host","hostid","flags","custom_interfaces","status"],"selectInterfaces": ["ip", "dns","useip","type","port"],"selectGroups": ["name"],"selectParentTemplates": ["name"],"sortfield": "host","sortorder": "ASC"})
    return hostsA


def get_hosts_zbx_dest():
    #Getting list of hosts zabbix server destination
    zapi = connect_zbx_dest()
    hostsB = zapi.host.get({"output": ["host"],"sortfield": "host","sortorder": "ASC"})
    return hostsB

def get_hostGroupSource():
    #Getting list of hostgoups zabbix server source
    zapi = connect_zbx_source()
    groupsA = zapi.hostgroup.get({"output": "extend"})
    return groupsA

def get_hostGroupDest(groupname):
    zapi = connect_zbx_dest()
    GetGroupsB = zapi.hostgroup.get({"output": ["name","groupid"],"filter": {"name": [groupname]}})
    if GetGroupsB == []:
        zapi.hostgroup.create({"name": groupname })
        groupcreated = zapi.hostgroup.get({"output": ["name","groupid"],"filter": {"name": [groupname]}})
        getGroupid = groupcreated[0]["groupid"]
        return getGroupid

    if len(GetGroupsB) == 1:
        getGroupid = GetGroupsB[0]["groupid"]
        return getGroupid

def create_hostsB_noiface(hostname,description):
    hostcriado = zapi.host.create({"host": hostname, "status": 0,"groups": [{"groupid": destHostGroup}],"description": description})
    return hostcriado

def create_hostsB_ip_ifagent(hostname,iftype,ip,description):
    hostcriado = zapi.host.create({"host": hostname, "status": 0,"interfaces": [{"type": iftype,"main": 1,"useip": 1,"ip": ip,"dns": "","port": "10050"}],"groups": [{"groupid": destHostGroup}],"description": description})
    return hostcriado

def create_hostsB_ipdns_ifagent(hostname,iftype,ipdns,description):
    hostcriado = zapi.host.create({"host": hostname, "status": 0,"interfaces": [{"type": iftype,"main": 1,"useip": 0,"ip": "","dns": ipdns,"port": "10050"}],"groups": [{"groupid": destHostGroup}],"description": description})
    return hostcriado

def create_hostsB_ip_ifacesnmp(hostname,ip,description):
    hostcriado = zapi.host.create({"host": hostname,"status": 0,"interfaces": [{"type": "2","main": 1,"useip": 1,"ip": ip,"dns": "","port": "161","details":{"version":"2","bulk":"1","community": "{$SNMP_COMMUNITY}"}}],"groups":[{"groupid": destHostGroup}],"description": description})
    return hostcriado

def create_hostsB_ipdns_ifacesnmp(hostname,ipdns,description):
    hostcriado = zapi.host.create({"host": hostname,"status": 0,"interfaces": [{"type": "2","main": 1,"useip": 0,"ip": "","dns": ipdns,"port": "161","details":{"version":"2","bulk":"1","community": "{$SNMP_COMMUNITY}"}}],"groups":[{"groupid": destHostGroup}],"description": description})
    return hostcriado

def create_hostsB_ip_ifaceipmi(hostname,ip,description):
    hostcriado = zapi.host.create({"host": hostname,"status": 0,"interfaces": [{"type": "3","main": 1,"useip": 1,"ip": ip,"dns": "","port": "623"}],"groups":[{"groupid": destHostGroup}],"description": description})
    return hostcriado

def create_hostsB_ipdns_ifaceipmi(hostname,ipdns,description):
    hostcriado = zapi.host.create({"host": hostname,"status": 0,"interfaces": [{"type": "3","main": 1,"useip": 0,"ip": "","dns": ipdns,"port": "623"}],"groups":[{"groupid": destHostGroup}],"description": description})
    return hostcriado

def create_hostsB_ip_ifacejmx(hostname,ip,description):
    hostcriado = zapi.host.create({"host": hostname,"status": 0,"interfaces": [{"type": "4","main": 1,"useip": 1,"ip": ip,"dns": "","port": "12345"}],"groups":[{"groupid": destHostGroup}],"description": description})
    return hostcriado

def create_hostsB_ipdns_ifacejmx(hostname,ipdns,description):
    hostcriado = zapi.host.create({"host": hostname,"status": 0,"interfaces": [{"type": "4","main": 1,"useip": 0,"ip": "","dns": ipdns,"port": "12345"}],"groups":[{"groupid": destHostGroup}],"description": description})
    return hostcriado

# Variables
destHostGroup = get_hostGroupDest(zbxgrouptomigrate)
hostlistA = []
hostlistB = []

for b in get_hosts_zbx_dest():
    hostname = b['host']
    hostlistB.append(hostname)

print("\nTotal hosts Zabbix server source: ",len(get_hosts_zbx_source()))
print("Total hosts Zabbix server dest: ",len(hostlistB),"\n")

print("########## Getting and importing hosts ##########\n")

zapi = connect_zbx_dest()
for h in get_hosts_zbx_source():
    hostname = h['host']
    grouplist = h['groups']
    hoststatus = h['status']
    for status in hoststatus:
        if int(status) == 0:
            hoststatus = "monitored host"
        else:
            hoststatus = "unmonitored host"
   
    templatelist = h['parentTemplates']
    if templatelist == []:
        templatelist = "Host without template!"
   
    description = ("Templates list: "+(str(templatelist)+"\nHost Status: "+hoststatus+"\nGroups: "+str(grouplist)))
    zbxhostid = h['hostid']
    custominterface = h['custom_interfaces']
    hostflag = h['flags']
    hostnotinterface = h['interfaces']

    if hostname in hostlistB:
         print("--- Host exist in zabbix server B: ",hostname)

    elif hostnotinterface == []:
        print(">>>>> Import",hostname," - ","no interface - host added"," to zabbix server B.")
        create_hostsB_noiface(hostname,description)

    else:
        iftype = h['interfaces'][0]['type']
        ifuseip = h['interfaces'][0]['useip']
        hostport = h['interfaces'][0]['port']
        ip = h['interfaces'][0]['ip']
        ipdns = h['interfaces'][0]['dns']

        if iftype == '1' and ifuseip == '1' and hostflag == '0':
            print(">>>>> Importing",hostname," - ",ip,":",hostport," to zabbix server B.")
            create_hostsB_ip_ifagent(hostname,iftype,ip,description)
        
        if iftype == '1' and ifuseip == '1' and hostflag == '4':
            if len(ip) and len(ipdns) == 0:
                print(">>>>> Importing",hostname," - ",ip,":",hostport," to zabbix server B.")
                create_hostsB_ip_ifagent(hostname,iftype,ip,description)
            else:
                create_hostsB_noiface(hostname,description)

        if iftype == '1' and ifuseip == '0':
            print(">>>>> Importing",hostname," - ",ipdns,":",hostport," to zabbix server B.")
            create_hostsB_ipdns_ifagent(hostname,iftype,ipdns,description)

        if iftype == '2' and ifuseip == '0':
            print(">>>>> Importing",hostname," - ",ipdns,":",hostport," to zabbix server B.")
            create_hostsB_ipdns_ifacesnmp(hostname,ipdns,description)

        if iftype == '2' and ifuseip == '1':
            print(">>>>> Importing",hostname," - ",ip,":",hostport," to zabbix server B.")
            create_hostsB_ip_ifacesnmp(hostname,ip,description)

        if iftype == '3' and ifuseip == '0':
            print(">>>>> Importing",hostname," - ",ipdns,":",hostport," to zabbix server B.")
            create_hostsB_ipdns_ifaceipmi(hostname,ipdns,description)

        if iftype == '3' and ifuseip == '1':
            print(">>>>> Importing",hostname," - ",ip,":",hostport," to zabbix server B.")
            create_hostsB_ip_ifaceipmi(hostname,ip,description)

        if iftype == '4' and ifuseip == '0':
            print(">>>>> Importing",hostname," - ",ipdns,":",hostport," to zabbix server B.")
            create_hostsB_ipdns_ifacejmx(hostname,ipdns,description)

        if iftype == '4' and ifuseip == '1':
            print(">>>>> Importing",hostname," - ",ip,":",hostport," to zabbix server B.")
            create_hostsB_ipdns_ifacejmx(hostname,ip,description)


for b in get_hosts_zbx_dest():
    hostname = b['host']
    hostlistB.append(hostname)

print("\nGetting total host list Zabbix server source: ",len(get_hosts_zbx_source()))
print("Getting total host list Zabbix server dest: ",len(hostlistB),"\n")