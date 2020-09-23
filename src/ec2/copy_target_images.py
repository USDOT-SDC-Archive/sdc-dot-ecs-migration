import logging
import pprint
import boto3
import json
from src.utils import awsutils
from botocore.exceptions import ClientError


def copy_target_amis(client, lst, KmsKeyId, waitForCompletion=False, DryRun=True):

    res_lst = []
    amis = []

    for elt in lst:
        instance_id = elt[0]
        tags = elt[1]
        description = tags["Name"]
        encrypted = True
        kms_key_id = KmsKeyId
        name = "ECS_RESTORED " + " " + instance_id + " " + tags["Name"]
        source_image_id = elt[3]
        source_region = 'us-east-1'


        res = client.copy_image(Description = description,
                                Encrypted = encrypted,
                                KmsKeyId = kms_key_id,
                                DryRun = DryRun,
                                Name = name,
                                SourceImageId = source_image_id,
                                SourceRegion = source_region)
        ami_id = res["ImageId"]
        pprint.pprint(ami_id)

        res_lst.append((elt[0], elt[1], elt[2], elt[3], ami_id))
        amis.append(ami_id)

    if waitForCompletion:
        awsutils.wait_for_ami_completion(client, amis)

    return res_lst


# main
def main(waitForCompletion = False):
    pprint.pprint("Entering copy_target_images.main()")
    vars = awsutils.read_vars()
    client = awsutils.get_ec2_client('us-east-1')

    with open('input/copied_amis.txt') as infile:
        lst = json.load(infile)

    #pprint.pprint(vars['KmsKeyId'])

    copied_amis = copy_target_amis(client,
                                   lst,
                                   waitForCompletion = waitForCompletion,
                                   KmsKeyId=vars['TargetKmsKeyId'],
                                   DryRun=False)

    with open('input/copied_target_amis.txt', 'w') as outfile:
        json.dump(copied_amis, outfile, indent=4)

    pprint.pprint("Leaving copy_target_images.main()")


#main()
