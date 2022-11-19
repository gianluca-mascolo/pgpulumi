"""A Python Pulumi program"""

import pulumi

import pulumi_postgresql as postgresql
import pulumi_random as random
from pulumi import Output
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
    userpassword=random.RandomPassword(f"{username}-password",length=20)
    postgresql.Role(resource_name=f"{username}-role",name=username,login=True,password=userpassword.result)
    #userpasswordoutput=userpassword.get(resource_name=f"{username}-password-output",id=f"{username}-password")
    #random.RandomPassword.get(resource_name=f"{username}-password-output",id=f"{username}-password")
    # userpasswordouput=str(Output.all(userpassword).apply(lambda result: f"{result}"))
    # pulumi.export(
    #     f"{username}-credentials",
    #     f"{username}:{userpasswordouput}"
    # )
# for g in dbgroups:
#     print(g["name"])
#     print(g["users"][0])
#     print(g["database"][0]["name"])

