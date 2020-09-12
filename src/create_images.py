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


def repackage_instances(instances):
    lst = []

    for i in instances:
        id = i["InstanceId"]
        tags = {}
        tags["InstanceType"] = i["InstanceType"]
        for t in i["Tags"]:
            tags[t["Key"]] = t["Value"]

        elt = (id, tags)
        lst.append(elt)

    return lst


def create_amis(client, lst, name_prefix, DryRun=True, NoReboot=True):

    res_lst = []
    #pprint.pprint(lst)
    for elt in lst:
        tags = elt[1]
        description = tags["Name"]
        instance_id = elt[0]
        name = name_prefix + tags["Name"]
        no_reboot = NoReboot

        res = client.create_image(Description = description,
                                  DryRun = DryRun,
                                  InstanceId = instance_id,
                                  Name = name,
                                  NoReboot = no_reboot)
        ami_id = res["ImageId"]
        pprint.pprint(ami_id)

        res_lst.append((elt[0], elt[1], ami_id))

    return res_lst


# main
def main():
    vars = awsutils.read_vars()
    client = awsutils.get_ec2_client('us-east-1')

    instances_file = "input/" + vars["InstancesInputFile"]
    with open(instances_file) as infile:
        instance_ids = json.load(infile)

    instances = get_instances(client, instance_ids)
    #pprint.pprint(instances)
    lst = repackage_instances(instances)

    base_amis = create_amis(client, lst,
                            vars["EcsQuarantineCopiedPrefix"],
                            DryRun=False, NoReboot=True)

    with open('input/base_amis.txt', 'w') as outfile:
        json.dump(base_amis, outfile, indent=4)


main()