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
for group in dbgroups:
    allusers.extend(group["users"])
    postgresql.Role(resource_name=f"{group['name']}-group-role",name=group["name"],login=False)
allusers=set(allusers)

for username in allusers:
    userpassword=random.RandomPassword(f"{username}-password",length=8,special=False)
    userroles=[group["name"] for group in dbgroups if username in group["users"] ]
    postgresql.Role(resource_name=f"{username}-role",name=username,login=True,password=userpassword.result,roles=userroles)
    if debug:
        Output.all(username,userpassword.result).apply(lambda args: write_to_file(u=args[0],p=args[1]))
