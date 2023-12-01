"""
Script: Change Hostname - Nornir + Napalm + Filter + Netbox 
Author: William Prado
Email: wprado@nic.br
"""

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_config, netmiko_commit
import os

def nornir_netmiko_send_config(task):
    configurations = ["hostname "+str(task.host.name)]
    command = task.run(netmiko_send_config, config_commands=configurations)
    print_result(command)
    commit = task.run(netmiko_commit)
    print_result(commit)

nr = InitNornir(
    runner={"plugin": "threaded", "options": {"num_workers": 20}},
    inventory={
         "plugin": "NetBoxInventory2",
          "options": {
             "nb_url": os.getenv("NETBOX_URL"),
             "nb_token": os.getenv("NETBOX_TOKEN"),
             "filter_parameters": {"tenant": ["production"], 
                                   "role": ["l2","pe","p"], 
                                   "region": ["sp","pr","rj","mg"], 
                                   "status": "active", 
                                   "platform": ["iosxr"]},
             "ssl_verify": False}})

nr.inventory.defaults.username = os.getenv("USER")
nr.inventory.defaults.password = os.getenv("PASSWORD")
nr.inventory.defaults.port = os.getenv("SSH_PORT")

nr.run(task=nornir_netmiko_send_config)
