"""
Script: Get Interfaces - Nornir + Napalm + Filter
Author: William Prado
Email: wprado@nic.br
"""

from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_rich.functions import print_result

nr = InitNornir(
  runner={"plugin": "threaded", "options": {"num_workers": 20}},
  config_file="hosts.yaml")

r2 = nr.filter(name="R2")

print_result(r2.run(task=napalm_get, getters=["get_interfaces"]), vars=["result"])
