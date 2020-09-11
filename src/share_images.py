import logging
import pprint
import boto3
import json
import awsutils
from botocore.exceptions import ClientError

#logger = logging.getLogger(__name__)
#ec2 = boto3.resource('ec2')

def share_amis(client, lst, TargetAccount, DryRun=True):

    res_lst = []
    #pprint.pprint(lst)
    for elt in lst:
        image_id = elt[3]

        res = client.modify_image_attribute(Attribute = 'launchPermission',
                                            ImageId = image_id,
                                            OperationType = 'add',
                                            UserIds = [TargetAccount],
                                            DryRun = DryRun)

        res_lst.append((image_id, res))

    return res_lst


# main
def main():
    vars = awsutils.read_vars()
    client = awsutils.get_ec2_client('us-east-1')

    with open('input/copied_amis.txt') as infile:
        lst = json.load(infile)

    #pprint.pprint(vars['KmsKeyId'])

    res = share_amis(client, lst, DryRun=False,
                            TargetAccount=vars['TargetAccount'])

    pprint.pprint(res)


main()