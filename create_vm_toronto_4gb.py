#!/usr/bin/env python
from lndynamic import LNDynamic
import natsort
import time

# find lunanode credentials
with open(r"/home/hme/.lunanode/commands.txt") as hpass:
    lines = hpass.readlines()
api = LNDynamic(lines[0].rstrip('\n'), lines[1].rstrip('\n'))

def create_master_cluster(name):
    api.request("vm", "create",
                {'hostname': name, 'plan_id': 88, 'region': 'toronto', 'image_id': 304052, 'storage': 70})

cluster_name = 'aston-docker-'
number_of_vm = input("Nbr_of_cluster ? ")

for i in range(3, int(number_of_vm) + 1):
    create_master_cluster(cluster_name  + str(i))


