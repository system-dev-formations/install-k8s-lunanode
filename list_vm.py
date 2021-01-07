#! /usr/bin/env python
from lndynamic import LNDynamic

with open(r"/home/hme/.lunanode/commands.txt") as hpass:
    lines = hpass.readlines()

api = LNDynamic(lines[0].rstrip('\n'), lines[1].rstrip('\n'))
results = api.request('vm', 'list')
#print(results)
val= results.get('vms')
#print(val)
for v in val:
    print("{}, {}".format(v['name'],v['region']))
    #ret = api.request('vm','shelve',{'vm_id': v['vm_id']})
    #print(ret)
results = api.request('vm', 'info', {'vm_id': '66d1d1f1-e837-4340-b3be-a58709d940e2'})
#print(results)

results = api.request('image', 'list')
print(results)