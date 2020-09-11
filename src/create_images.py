import logging
import pprint
import boto3
import json
import awsutils
from botocore.exceptions import ClientError

#logger = logging.getLogger(__name__)
#ec2 = boto3.resource('ec2')

def create_amis(client, lst, DryRun=True, NoReboot=True):

    res_lst = []
    #pprint.pprint(lst)
    for elt in lst:
        tags = elt[1]
        description = tags["Name"]
        instance_id = elt[0]
        name = tags["Name"]
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
    client = awsutils.get_ec2_client('us-east-1')

    with open('input/instances.txt') as infile:
        instance_ids = json.load(infile)

    instances = awsutils.get_instances(client, instance_ids)
    lst = awsutils.repackage_instances(instances)

    #pprint.pprint(lst)

    base_amis = create_amis(client, lst, DryRun=False, NoReboot=True)

    with open('input/base_amis.txt', 'w') as outfile:
        json.dump(base_amis, outfile)


#main()