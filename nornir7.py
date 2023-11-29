"""
Script: Change Configuration - Nornir + Napalm + Netmiko + Netbox (API)
Author: William Prado
Email: wprado@nic.br
"""

from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_netmiko.tasks import netmiko_send_config, netmiko_commit
from nornir_rich.functions import print_result
import requests, os

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Token '+str(os.getenv("NETBOX_TOKEN"))
}

def nornir_netmiko_configure(task):
    try:
        data_device = task.run(task=napalm_get, getters=["get_interfaces"])
        data_device = data_device.result['get_interfaces']
        
        url_netbox = str(os.getenv("NETBOX_URL"))+"/api/dcim/interfaces/?device="+str(task.host)
        response_device = requests.request("GET", url_netbox, headers=headers, verify=False)
        
        for interface_netbox in response_device.json()['results']:
            configurations=["interface "+str(interface_netbox['name'])]
            if data_device[interface_netbox['name']]['is_enabled'] != interface_netbox['enabled']:
                if interface_netbox['enabled'] == True:
                    configurations.append("no shutdown")
                if interface_netbox['enabled'] == False:
                    configurations.append("shutdown")
            if data_device[interface_netbox['name']]['description'] != interface_netbox['description']:
                if interface_netbox['description'] == "":
                    configurations.append("no description")
                else:        
                    configurations.append("description "+str(interface_netbox['description']))
            if data_device[interface_netbox['name']]['mtu'] != interface_netbox['mtu']:
                configurations.append("mtu "+str(interface_netbox['mtu']))
            if len(configurations) > 1:
                command = task.run(netmiko_send_config, config_commands=configurations)
                print_result(command)
                commit = task.run(netmiko_commit)
                print_result(commit)
    except Exception as err:
        print(err)
        
        
        
   
nr = InitNornir(
    inventory={
         "plugin": "NetBoxInventory2",
          "options": {
             "nb_url": os.getenv("NETBOX_URL"),
                "nb_token": os.getenv("NETBOX_TOKEN"),
             "filter_parameters": {"name": "poppr-pe-ncs5501-103"},
             "ssl_verify": False}})

nr.inventory.defaults.username = os.getenv("USER")
nr.inventory.defaults.password = os.getenv("PASSWORD")
nr.inventory.defaults.port = os.getenv("SSH_PORT")

nr.run(task=nornir_netmiko_configure)
