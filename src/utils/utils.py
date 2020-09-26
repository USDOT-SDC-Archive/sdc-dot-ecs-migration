# awsutils

import boto3
import json
import time
import datetime
import pprint


def get_src_users_instances_map():
    with open('../dynamo_db/input/src-users-instances-raw.txt') as f:
        lines = f.read().splitlines()

    dct = {}
    for kv in lines:
        k = kv.split()[0]
        v = kv.split()[1]

        if k in dct.keys():
            dct[k].append(v)
        else:
            dct[k] = [ v ]

    with open('../dynamo_db/input/src-users-instances-to-migrate.txt', 'w') as f:
        f.write(json.dumps(dct, indent=4))

    return dct


def get_src_instances():
    with open('../dynamo_db/input/src-users-instances-raw.txt') as f:
        lines = f.read().splitlines()

    ec2s = []
    for kv in lines:
        ec2 = kv.split()[1]

        if not ec2 in ec2s:
            ec2s.append(ec2)

    return ec2s


def map_s3_to_ecs_prod():
    with open('../dynamo_db/input/s3-map-raw.txt') as f:
        lines = f.read().splitlines()

    dct = {}
    for kv in lines:
        k = kv.split()[0]
        v = kv.split()[1]

        dct[k] = v

    return dct


def map_ec2_to_ecs_prod():
    with open('../dynamo_db/input/dynamo_target_ec2s.txt') as infile:
        lst = json.load(infile)

    dct = {}
    for elt in lst:
        k = elt[0]
        v = elt[5]

        dct[k] = v

    return dct

def map_ec2_to_ecs_prod_simple():
    with open('../dynamo_db/input/simple_target_ec2s.txt') as infile:
        lst = json.load(infile)

    return lst

