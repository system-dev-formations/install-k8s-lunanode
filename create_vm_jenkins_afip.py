#!/usr/bin/env python

import natsort
import time

from lndynamic import LNDynamic

# find lunanode credentials
with open(r"../../afip_luna.txt") as hpass:
      lines = hpass.readlines()
api = LNDynamic(lines[0].rstrip('\n'), lines[1].rstrip('\n'))

# image Centos-controller
def create_centos_jenkins(name):
    api.request("vm", "create",
                {'hostname': name, 'plan_id': 90, 'region': 'toronto', 'image_id': 148497, 'storage': 125})
project_name = 'afip-jenkins-'
user_number = input("Nombre de vm ? ")
for x in range(4, int(user_number)):
    user_number= str(x+1)
    print(project_name+user_number)
    create_centos_jenkins(project_name +  user_number)



