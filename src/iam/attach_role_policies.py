import pprint
import boto3
import json
from botocore.exceptions import ClientError

from src.utils import utils
from src.utils import awsutils
from src.ec2 import describe_instances


def attach_role_policies(client, vars, dct):

    for role_name, role_elt in dct.items():
        for policy in role_elt['AttachedPolicies']:

            try:
                res = client.attach_role_policy(RoleName=role_name,
                                         PolicyArn=policy['PolicyArn'])

                pprint.pprint(res)

            except ClientError as e:
                raise e

        samba_share_policy_arn = vars['SambaSharePolicy']
        try:
            res = client.attach_role_policy(RoleName=role_name,
                                            PolicyArn=samba_share_policy_arn)

            pprint.pprint(res)

        except ClientError as e:
            raise e

    return dct


def main():
    vars = awsutils.read_vars()
    iam = boto3.client('iam')
    with open('input/created-roles.txt') as infile:
        dct = json.load(infile)

    res = attach_role_policies(iam, vars, dct)

    return res


if __name__ == '__main__':
    main()


