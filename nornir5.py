"""
Script: Change NTP Server - Nornir + Napalm + Filter + Netbox + Config Contexts
Author: William Prado
Email: wprado@nic.br
"""

from nornir import InitNornir
from nornir_netmiko import netmiko_send_config, netmiko_commit
from nornir_rich.functions import print_result
import os

def nornir_netmiko_send_config(task):
    host_inventory = nr.inventory.hosts[task.host.name]
    ntp_server = host_inventory['config_context']['ntp_servers'][0]
    router = nr.filter(name=str(task.host.name))
    configurations = ["ntp server vrf mgmt-vrf "+str(ntp_server)]
    router.run(netmiko_send_config, config_commands=configurations)
    router.run(netmiko_commit)

nr = InitNornir(
    runner={"plugin": "threaded", "options": {"num_workers": 20}},
    inventory={
        "plugin": "NetBoxInventory2",
        "options": {
            "nb_url": os.getenv("NETBOX_URL"),
            "nb_token": os.getenv("NETBOX_TOKEN"),
            "filter_parameters": {"tenant": "production", 
                                  "role": ["l2","pe","p"],
                                  "region": ["sp","pr","rj","mg"],
                                  "status": "active",
                                  "platform": "iosxr"},
            "ssl_verify": False}})

nr.inventory.defaults.username = os.getenv("USER")
nr.inventory.defaults.password = os.getenv("PASSWORD")
nr.inventory.defaults.port = os.getenv("SSH_PORT")

print_result(nr.run(task=nornir_netmiko_send_config), vars=["result"])
