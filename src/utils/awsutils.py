# awsutils

import boto3
import json
import time
import datetime
import pprint

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


def read_vars(file = '../input/vars.txt'):
    with open(file) as infile:
        vars = json.load(infile)
    return vars


def write_vars():
    vars = {'SourceKmsKeyId': 'alias/XXX',
            'TargetKmsKeyId': 'alias/XXX',
            'TargetAccount': 'XXXS'}

    with open('input/vars.txt', 'w') as outfile:
        json.dump(vars, outfile, indent=4)


def wait_for_ami_completion(client, amis):
    completed = False
    total = str(len(amis))

    while not completed:
        res = client.describe_images(ImageIds=amis)

        remaining = 0
        s = ""
        for ami in res["Images"]:
            s += ami["ImageId"] + ": " + ami["State"] + ", "
            if ami["State"] != 'available' and ami["State"] != 'failed':
                remaining += 1

        pprint.pprint(s)
        pprint.pprint(str(datetime.datetime.now()) + " total: " + total + ", remaining: " + str(remaining))
        if remaining == 0:
            completed = True

        if not completed:
            time.sleep(30)

    #pprint.pprint(res)

def test_wait_for_ami_completion():
    client = get_ec2_client('us-east-1')
    wait_for_ami_completion(client, ['ami-04458ff99aa4fa50d', 'ami-019028be06ac41998'])


#write_vars()
#test_wait_for_completion()