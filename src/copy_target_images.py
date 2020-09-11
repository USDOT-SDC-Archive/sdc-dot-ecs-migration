import logging
import pprint
import boto3
import json
import awsutils
from botocore.exceptions import ClientError

#logger = logging.getLogger(__name__)
#ec2 = boto3.resource('ec2')

def copy_target_amis(client, lst, KmsKeyId, DryRun=True):

    res_lst = []
    #pprint.pprint(lst)
    for elt in lst:
        instance_id = elt[0]
        tags = elt[1]
        description = tags["Name"]
        encrypted = True
        kms_key_id = KmsKeyId
        name = "SHARED " + tags["Name"]
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

    return res_lst


# main
def main():
    vars = awsutils.read_vars()
    client = awsutils.get_ec2_client('us-east-1')

    with open('input/copied_amis.txt') as infile:
        lst = json.load(infile)

    #pprint.pprint(vars['KmsKeyId'])

    copied_amis = copy_target_amis(client, lst, DryRun=True,
                            KmsKeyId=vars['TargetKmsKeyId'])

    with open('input/copied_target_amis.txt', 'w') as outfile:
        json.dump(copied_amis, outfile, indent=4)


main()