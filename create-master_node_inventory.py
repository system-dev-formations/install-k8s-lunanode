#!/usr/bin/env python
import os

inventory= open(r"/home/hme/inventory_lunanode" ,"r")
invent= inventory.readlines()
user_list= open(r"/home/hme/user_list" ,"r")
user=user_list.readlines()
inventory_k8s= open(r"/home/hme/inventory_k8s" ,"w+")

inventory_k8s.write("[master]")
for i in user:
    print(i)
