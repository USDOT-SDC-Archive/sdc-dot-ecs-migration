# awsutils

import boto3
import json

def get_session(region):
    return boto3.session.Session(region_name=region)

def get_ec2_client(region):
    session = get_session(region)
    return session.client('ec2')

def get_instances(client, instance_ids):
    instances = client.describe_instances(InstanceIds=instance_ids)

    all = []

    # re-package into a flat list
    for r in instances["Reservations"]:
        for i in r["Instances"]:
            all.append(i)

    return all


def repackage_instances_as_dct(instances):
    dct = {}

    for i in instances:
        id = i["InstanceId"]
        tags = {}
        for t in i["Tags"]:
            tags[t["Key"]] = t["Value"]
            dct[id] = tags

    return dct

def repackage_instances(instances):
    lst = []

    for i in instances:
        id = i["InstanceId"]
        tags = {}
        for t in i["Tags"]:
            tags[t["Key"]] = t["Value"]

        elt = (id, tags)
        lst.append(elt)

    return lst

def read_vars():
    with open('input/vars.txt') as infile:
        vars = json.load(infile)
    return vars


def write_vars():
    vars = {'SourceKmsKeyId': 'alias/XXX',
            'TargetKmsKeyId': 'alias/XXX',
            'TargetAccount': 'XXXS'}

    with open('input/vars.txt', 'w') as outfile:
        json.dump(vars, outfile, indent=4)


#write_vars()