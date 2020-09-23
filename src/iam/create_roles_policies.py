import pprint
import boto3
import json
from botocore.exceptions import ClientError

from src.utils import utils
from src.utils import awsutils
from src.ec2 import describe_instances


def list_roles():
    src_ec2s = utils.get_src_instances()

    ec2client = boto3.client('ec2')

    instances = describe_instances.get_instances(ec2client, src_ec2s)

    roles = []
    for i in instances:
        roleName = i["IamInstanceProfile"]["Arn"].rpartition('/')[-1]
        #pprint.pprint(roleName + ' --> ' + i['InstanceId'])

        if not roleName in roles:
            roles.append(roleName)

    return roles


def main():
    vars = awsutils.read_vars()
    roles = list_roles()

    iam = boto3.client('iam')

    for role in roles:
        #role_res = iam.get_role(RoleName = role)
        role_policies_res = iam.list_attached_role_policies(RoleName = role)
        pprint.pprint(role_policies_res)

    #res = iam.get_policy(PolicyArn = 'arn:aws:iam::911061262852:policy/prod-sdc-cross-sdc-bucket-policy')
    #policy = res['Policy']
    #res = iam.get_policy_version(
    #    PolicyArn = policy['Arn'],
    #    VersionId = policy['DefaultVersionId']
    #)

    #pprint.pprint(res)
    #pprint.pprint(res['Role'])
    #return response['Item']


if __name__ == '__main__':
    main()


