# awsutils

import boto3
import json


def get_session(region):
    return boto3.session.Session(region_name=region)


def get_ec2_client(region):
    session = get_session(region)
    return session.client('ec2')


def get_instance_tags(instance):
    tags = {}
    for t in instance["Tags"]:
        tags[t["Key"]] = t["Value"]

    return tags


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