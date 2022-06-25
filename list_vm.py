#! /usr/bin/env python
from lndynamic import LNDynamic

with open(r"../../system-dev.txt") as hpass:
    lines = hpass.readlines()

api = LNDynamic(lines[0].rstrip('\n'), lines[1].rstrip('\n'))
results = api.request('vm', 'list')
print(results)
val= results.get('vms')
#print(val)
#for v in val:
#    print("{}, {}".format(v['name'],v['region']))
#    #ret = api.request('vm','shelve',{'vm_id': v['vm_id']})
#    #print(ret)
results = api.request('vm', 'info', {'vm_id': 'f680cd48-000f-42b8-ba30-65c0d7c814df'})
#print(results)
print("-------------------------------")
results = api.request('image', 'list')
print(results)