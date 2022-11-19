"""A Python Pulumi program"""

import pulumi

import pulumi_postgresql as postgresql
import pulumi_random as random

conf = pulumi.Config("pgpulumi")
dblist = conf.require_object("databases")
dbgroups = conf.require_object("groups")

for db in dblist:
    postgresql.Database(resource_name=db,name=db)

allusers=[]
for g in dbgroups:
    allusers.extend(g["users"])
allusers=set(allusers)

for username in allusers:
    postgresql.Role(resource_name=f"{username}-role",name=username,login=True,password=random.RandomPassword(f"{username}-password",length=20))
# for g in dbgroups:
#     print(g["name"])
#     print(g["users"][0])
#     print(g["database"][0]["name"])

