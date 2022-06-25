#!/usr/bin/env python

import natsort
import time

from lndynamic import LNDynamic

# find lunanode credentials
with open(r"../../system-dev.txt") as hpass:
      lines = hpass.readlines()
api = LNDynamic(lines[0].rstrip('\n'), lines[1].rstrip('\n'))

# image Centos-controller
def create_centos_jenkins(name):
    api.request("vm", "create",
                #{'hostname': name, 'plan_id': 90, 'region': 'toronto', 'image_id': 148497, 'storage': 125})
                #{'hostname': name, 'plan_id': 90, 'region': 'toronto', 'image_id': 304052, 'storage': 125})  # 16 gb .ubuntu 20.04
                #{'hostname': name, 'plan_id': 64, 'region': 'montreal', 'image_id': 304057, 'storage': 125})  # 16 gb . ubuntu 20.4
                {'hostname': name, 'plan_id': 62, 'region': 'montreal', 'image_id': 304057, 'storage': 35})  # 4 Gb , ubuntu 20.4
project_name = 'aston-awx-remote-'
user_number = input("Nombre de vm ? ")
for x in range(1, int(user_number)):
    user_number= str(x)
    print(project_name+user_number)
    create_centos_jenkins(project_name +  user_number)



