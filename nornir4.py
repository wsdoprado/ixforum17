"""
Script: Get Interface - Nornir + Napalm + Filter + Netbox
Author: William Prado
Email: wprado@nic.br
"""

from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_rich.functions import print_result
import os

nr = InitNornir(
        runner={"plugin": "threaded", "options": {"num_workers": 20}},
        inventory={
            "plugin": "NetBoxInventory2",
            "options": {
                "nb_url": os.getenv("NETBOX_URL"),
                "nb_token": os.getenv("NETBOX_TOKEN"),
                "filter_parameters": {
                    "tenant": "production", 
                    "role": "l2", 
                    "region": "mg", 
                    "status": "active", 
                    "platform": "iosxr"},
                "ssl_verify": False}
        })

nr.inventory.defaults.username = os.getenv("USER")
nr.inventory.defaults.password = os.getenv("PASSWORD")
nr.inventory.defaults.port = os.getenv("SSH_PORT")

print_result(nr.run(task=napalm_get, getters=["get_interfaces"]), vars=["result", "name"])
