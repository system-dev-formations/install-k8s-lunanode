#!/usr/bin/env python
from lndynamic import LNDynamic
import natsort
import time

# find lunanode credentials
with open(r"/home/hme/.lunanode/commands.txt") as hpass:
    lines = hpass.readlines()
api = LNDynamic(lines[0].rstrip('\n'), lines[1].rstrip('\n'))
results = api.request('vm', 'list')
f = open(r"/home/hme/inventory_webforce3_docker", "w+")
hfile = open(r"/home/hme/user_list_webforce3_docker", "w+")
val = results.get("vms")
user_dic = {}
user_pass={}
len(val)
for i in range(0, len(val)):
    flag = 0
    for key, value in val[i].items():
        if key == 'name':
            #search= "-" + user_number
            if "docker" not in value:
                break
            print('name=', value)
            user = value
        if key == 'primaryip':
            ip = value
            print('ip=', value)
        if key == 'plan_id':
            print('plan_id=', value)
        if key == 'vm_id':
            print('vm_id=', value)
            vm_info = api.request('vm', 'info', {'vm_id': value})
            st = vm_info.get('info')
            try:
                print(st['login_details'])
                user_login = st['login_details']
                a = user_login.split()
                print(str(ip), str(a[1]), str(a[3]))
                gt = str(a[1])[:-1]
                line = "{}  ansible_ssh_user={}  ansible_ssh_pass={} ansible_ssh_extra_args='-o StrictHostKeyChecking=no'\n".format(
                    str(ip), str(gt), str(a[3]))
                f.write(line)
                user_dic[str(user)] = str(ip)
                user_pass[str(user)]= str(a[3])
            except KeyError as error:
                pass

f.close()
print (user_dic)
list_user = user_dic.keys();
natural = natsort.natsorted(list_user)
print(natural)
for vts in range(0, len(natural)):
    myip = user_dic[natural[vts]]
    mypass =  user_pass[natural[vts]]
    user_line = "{} \t {} \t {} \n".format(natural[vts], myip, mypass)
    hfile.write(user_line)
hfile.close()