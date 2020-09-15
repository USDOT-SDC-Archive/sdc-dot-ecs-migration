import logging
import pprint
import boto3
import json
import awsutils
from botocore.exceptions import ClientError

#logger = logging.getLogger(__name__)
#ec2 = boto3.resource('ec2')

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


# main
def main():
    vars = awsutils.read_vars()
    client = awsutils.get_ec2_client('us-east-1')

    instances_file = "input/" + vars["InstancesInputFile"]
    with open(instances_file) as infile:
        instance_ids = json.load(infile)

    instances = get_instances(client, instance_ids)
    #pprint.pprint(instances)

    for i in instances:
        tags = awsutils.get_instance_tags(i)
        s = i["InstanceId"] + " --> " + tags["OS"] + " --> " + json.dumps(i["State"]["Name"])
        pprint.pprint(s)


main()