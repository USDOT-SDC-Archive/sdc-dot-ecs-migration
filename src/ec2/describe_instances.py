import logging
import pprint
import boto3
import json
from src.utils import awsutils
from botocore.exceptions import ClientError

#logger = logging.getLogger(__name__)
#ec2 = boto3.resource('ec2')

def list_roles():
    instances = main()

    for i in instances:
        tags = awsutils.get_instance_tags(i)
        s = i["IamInstanceProfile"]["Arn"].rpartition('/')[-1]
        pprint.pprint(s)

    return instances


def get_instances(client, instance_ids, Verbose=True):
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

def get_launch_times(instances):
    launch_times = ''
    for i in instances:
        tags = awsutils.get_instance_tags(i)
        s = i["InstanceId"] + " --> " + tags["OS"] + " | " + i["PrivateIpAddress"] + \
            " --> " + json.dumps(i["State"]["Name"])
        pprint.pprint(s)
        launch_times = launch_times + i["InstanceId"] + ' ' + str(i['LaunchTime']) + '\n'

    return launch_times


# main
def main():
    vars = awsutils.read_vars()
    client = awsutils.get_ec2_client('us-east-1')

    instances_file = "input/" + vars["InstancesInputFile"]
    with open(instances_file) as infile:
        instance_ids = json.load(infile)

    instances = get_instances(client, instance_ids)
    pprint.pprint(instances)

    launch_times = get_launch_times(instances)
    pprint.pprint(launch_times)

    return instances


if __name__ == '__main__':
    main()

