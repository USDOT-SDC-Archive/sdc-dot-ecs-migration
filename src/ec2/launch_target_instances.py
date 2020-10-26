import logging
import pprint
import boto3
import json
from src.utils import awsutils
from botocore.exceptions import ClientError

#logger = logging.getLogger(__name__)
#ec2 = boto3.resource('ec2')

def get_tag_specifications(dct, name_prefix):
    dct["Name"] = name_prefix + dct["Name"]
    tags = []
    for k, v in dct.items():
        tags.append({ "Key": k, "Value": v })

    ts = [{ "ResourceType": "instance", "Tags": tags },
          {"ResourceType": "volume", "Tags": tags}]

    return ts

def launch_ec2s(client, lst, name_prefix, key_name, security_group_ids, subnet_id, DryRun=True):

    res_lst = []
    #pprint.pprint(lst)
    for elt in lst:
        tags = elt[1]
        image_id = elt[4]
        instance_type = tags["InstanceType"]
        tag_specifications = get_tag_specifications(tags, name_prefix)

        res = client.run_instances(ImageId = image_id,
                                   InstanceType = instance_type,
                                   KeyName = key_name,
                                   MaxCount = 1,
                                   MinCount = 1,
                                   SecurityGroupIds = security_group_ids,
                                   SubnetId = subnet_id,
                                   TagSpecifications=tag_specifications,
                                   DryRun = DryRun)

        res_lst.append((elt[0], elt[1], elt[2], elt[3], elt[4],
                        res["Instances"][0]["InstanceId"]))

    return res_lst


# main
def main():
    pprint.pprint("Entering launch_target_instances.main()")
    vars = awsutils.read_vars()
    client = awsutils.get_ec2_client('us-east-1')

    with open('input/copied_target_amis.txt') as infile:
        lst = json.load(infile)

    #pprint.pprint(vars['KmsKeyId'])

    instances = launch_ec2s(client,
                            lst,
                            vars["EcsRestoredPrefix"],
                            vars["EC2KeyName"],
                            vars["EC2SecurityGroupIds"],
                            vars["EC2SubnetId"],
                            DryRun=False)

    pprint.pprint(instances)
    with open('input/launched_target_ec2s.txt', 'w') as outfile:
        json.dump(instances, outfile, indent=4)

    pprint.pprint("Leaving launch_target_instances.main()")


if __name__ == '__main__':
    main()
