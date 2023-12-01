"""
Script: Show Interfaces Brief - Nornir + Netmiko + Filter
Author: William Prado
Email: wprado@nic.br
"""

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks.netmiko_send_command import netmiko_send_command

nr = InitNornir(
  runner={"plugin": "threaded", "options": {"num_workers": 20}},
  config_file="hosts.yaml")

r4 = nr.filter(name="R4")

results = r4.run(netmiko_send_command, command_string="show interfaces brief")

print_result(results)

