import logging
import pprint
import boto3
import json
from src.utils import awsutils
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


def get_snapshots(client, lst, DryRun=True):
    snapshots = []

    for elt in lst:
        image_id = elt[3]
        images = client.describe_images(ImageIds = [image_id],
                                     DryRun = DryRun)
        for ami in images["Images"]:
            for ebs in ami["BlockDeviceMappings"]:
                snapshots.append(ebs["Ebs"]["SnapshotId"])

    return snapshots


def share_snapshots(client, snapshots, TargetAccount, DryRun=True):
    res_lst = []

    for snapshot_id in snapshots:
        res = client.modify_snapshot_attribute(Attribute = 'createVolumePermission',
                                               SnapshotId = snapshot_id,
                                               OperationType = 'add',
                                               UserIds = [TargetAccount],
                                               DryRun = DryRun)
        res_lst.append(res)

    return res_lst


# main
def main():
    pprint.pprint("Entering share_images.main()")
    vars = awsutils.read_vars()
    client = awsutils.get_ec2_client('us-east-1')

    with open('input/copied_amis.txt') as infile:
        lst = json.load(infile)

    res = share_amis(client, lst, DryRun=False,
                            TargetAccount=vars['TargetAccount'])
    pprint.pprint(res)

    snapshots = get_snapshots(client, lst, DryRun=False)
    pprint.pprint(snapshots)

    res = share_snapshots(client, snapshots, vars['TargetAccount'], DryRun=False)
    pprint.pprint(res)
    pprint.pprint("Leaving share_images.main()")


#main()