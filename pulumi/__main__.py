"""A Python Pulumi program"""

import pulumi

import pulumi_postgresql as postgresql
import pulumi_random as random
from pulumi import Output
conf = pulumi.Config("pgpulumi")
dbgroups = conf.require_object("groups")
permissionsets = conf.require_object("permissionsets")

allusers=[]
group_resource={}
for group in dbgroups:
    allusers.extend(group["users"])
    group_name=group['name']
    group_resource[group_name]=postgresql.Role(resource_name=f"{group_name}-group-role",name=group_name,login=False)
    for db in group["databases"]:
        privileges=permissionsets[db["privileges"]]
        postgresql.Grant(
            resource_name=f'{group_name}-{db["name"]}-{db["privileges"]}-privileges',database=db["name"],
            object_type="table",
            privileges=privileges,
            role=group_resource[group_name].name,
            schema="public")

allusers=set(allusers)

for username in allusers:
    userpassword=random.RandomPassword(f"{username}-password",length=8,special=False)
    usergroups=[group["name"] for group in dbgroups if username in group["users"] ]
    postgresql.Role(
        resource_name=f"{username}-role",
        name=username,
        login=True,
        password=userpassword.result,
        roles=[group_resource[group_name].name for group_name in usergroups ]
        )
    pulumi.export(f"pwexport-{username}", userpassword.result)
