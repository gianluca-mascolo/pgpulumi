"""A Python Pulumi program"""

import pulumi

import pulumi_postgresql as postgresql

my_db = postgresql.Database(resource_name="my-database",name="my-database")
