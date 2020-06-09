from lndynamic import LNDynamic
import natsort
import time

# find lunanode credentials
with open(r"/home/hme/.lunanode/commands.txt") as hpass:
    lines = hpass.readlines()
api = LNDynamic(lines[0].rstrip('\n'), lines[1].rstrip('\n'))
f = open(r"/home/hme/inventory-ambient-docker", "w+")
hfile=open(r"/home/hme/users-ambient-docker", "w+")
# image Ubuntu-remote
def create_ubuntu_remote(name):
    api.request("vm", "create",
                {'hostname': name, 'plan_id': 5, 'region': 'roubaix', 'image_id': 240302, 'storage': 70})

project_name = 'ambient-'
user_number = input("Nombre de vm ? ")
max_vm = int(user_number)
for vm in range(1,max_vm):
    create_ubuntu_remote(project_name + "docker-" + str(vm))
time.sleep(240)
results = api.request('vm', 'list')
val= results.get('vms')
all_key= ['vm_id','name','primaryip']
#print(val)
user_dic={}
user='ubuntu'
f.write("[docker]\n")
for z in range(0,len(val)):
    if project_name in val[z].get(all_key[1]):
        #print(val[z].get(all_key[0]))
        name=val[z].get(all_key[1])
        #print(name)
        ip= val[z].get(all_key[2])
        results = api.request('vm', 'info', {'vm_id': val[z].get(all_key[0])})
        #print(results)
        thepass=results.get('info')
        part=thepass.get('login_details').split(':')
        password=part[2]
        line = "{} ansible_host={}  ansible_ssh_user={}  ansible_ssh_pass={} ansible_ssh_extra_args='-o StrictHostKeyChecking=no'\n".format(name, ip, user , password.strip())
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


