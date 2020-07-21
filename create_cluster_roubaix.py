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
                {'hostname': name, 'plan_id': 4, 'region': 'roubaix', 'image_id': 148540, 'storage': 70})
list_of_color=['iron']
#list_of_color= ['silver','green','blue','pink','yellow','purple','cyan','brown','magenta','amber']

#list_of_color= ['silver','green','black','blue','pink']
#list_of_color= ['yellow','purple','cyan','brown','magenta']
#list_of_color= ['amber','carmine']
#list_of_color=['black']
#list_of_color= ['green','black','blue']
for x in list_of_color:
    cluster_name = 'k8s-' + x
    create_master_cluster(cluster_name  + "-master")
    for j in range(1, 3):
        vm_name = cluster_name  + "-node-" + str(j)
        api.request("vm", "create",
                    {'hostname': vm_name, 'plan_id': 4, 'region': 'roubaix', 'image_id': 148540, 'storage': 70})
    # sleep while lunanode setting up public ip addresses for each VMs
    time.sleep(180)
    results = api.request('vm', 'list')
    f = open(r"/home/hme/inventory-" + cluster_name, "w+")
    hfile = open(r"/home/hme/user_list-" + cluster_name, "w+")
    val = results.get("vms")
    all_key= ['vm_id','name','primaryip']
    #print(val)
    user='ubuntu'
    for z in range(0,len(val)):
        if x in val[z].get(all_key[1]):
            #print(val[z].get(all_key[0]))
            name=val[z].get(all_key[1])
            ip= val[z].get(all_key[2])
            results = api.request('vm', 'info', {'vm_id': val[z].get(all_key[0])})
            thepass=results.get('info')
            part=thepass.get('login_details').split(':')
            password=part[2]
            line = "{}  ansible_ssh_user={}  ansible_ssh_pass={} ansible_ssh_extra_args='-o StrictHostKeyChecking=no'\n".format(ip, user , password.strip())
            f.write(line)
    f.close()
    # print (user_dic)
    #list_user = user_dic.keys();
    #natural = natsort.natsorted(list_user)
    # print natural
    #for vts in range(0, len(natural)):
    #    myip = user_dic[natural[vts]]
    #    user_line = "{} \t {} \t ubuntu \t lawn-vex \n".format(natural[vts], myip)
    #    hfile.write(user_line)
    #hfile.close()
