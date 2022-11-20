"""A Python Pulumi program"""

import pulumi

import pulumi_postgresql as postgresql
import pulumi_random as random
from pulumi import Output
conf = pulumi.Config("pgpulumi")
dblist = conf.require_object("databases")
dbgroups = conf.require_object("groups")
debug = conf.get_bool("debug") or False

def write_to_file(u,p):
    f = open("userlist.txt", "a")
    f.write(f"{u}:{p}\n")
    f.close()

allusers=[]
for g in dbgroups:
    allusers.extend(g["users"])
allusers=set(allusers)

for username in allusers:
    userpassword=random.RandomPassword(f"{username}-password",length=8,special=False)
    postgresql.Role(resource_name=f"{username}-role",name=username,login=True,password=userpassword.result)
    if debug:
        Output.all(username,userpassword.result).apply(lambda args: write_to_file(u=args[0],p=args[1]))
