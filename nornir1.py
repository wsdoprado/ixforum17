"""
Script: Show Interfaces Brief - Nornir + Netmiko
Author: Eng. William Prado
Email: wprado@nic.br
"""

from nornir import InitNornir
from nornir_rich.functions import print_result
from nornir_netmiko.tasks.netmiko_send_command import netmiko_send_command


nr = InitNornir(
  runner={"plugin": "threaded", "options": {"num_workers": 50}},
  config_file="hosts.yaml")


print_result(nr.run(netmiko_send_command, command_string="show interfaces brief"))


