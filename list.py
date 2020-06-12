#! /usr/bin/env python
from lndynamic import LNDynamic
import natsort
import time

with open(r"/home/hme/.lunanode/commands.txt") as hpass:
    lines = hpass.readlines()

f = open(r"/home/hme/inventory_paris_docker_skf", "w+")
hfile=open(r"/home/hme/users-paris-docker_skf", "w+")
api = LNDynamic(lines[0].rstrip('\n'), lines[1].rstrip('\n'))
results = api.request('vm', 'list')
val= results.get('vms')
all_key= ['vm_id','name','primaryip']
#print(val)
user='ubuntu'
user_dic={}
for z in range(0,len(val)):
        if "ambient-docker" in val[z].get(all_key[1]):
            #print(val[z].get(all_key[0]))
            name=val[z].get(all_key[1])
            #print(name)
            ip= val[z].get(all_key[2])
            results = api.request('vm', 'info', {'vm_id': val[z].get(all_key[0])})
            #print(results)
            thepass=results.get('info')
            part=thepass.get('login_details').split(':')
            password=part[2]
            line = "{} ansible_host={}  ansible_ssh_user={}  ansible_ssh_pass={} ansible_ssh_extra_args='-o StrictHostKeyChecking=no'\n".format(name, ip, user , password.strip() )
            user_dic[name]="ip={} user={} password={}".format(ip,"ubuntu",password.strip())
            f.write(line)
f.close()
list_user = user_dic.keys()
natural = natsort.natsorted(list_user)
for vts in range(0, len(natural)):
    myline = user_dic[natural[vts]]
    user_line = "{} \t {} \n".format(natural[vts], myline)
    hfile.write(user_line)
hfile.close()


#results = api.request('vm', 'info', {'vm_id': 'e3e7ab5c-a944-4118-bf78-8a67b4722c48'})
#print ("-----------------------")
#print (results)

#results = api.request('image', 'list')
#print(results)


#1c018f61-e116-46d2-8a64-18f6963e3be7