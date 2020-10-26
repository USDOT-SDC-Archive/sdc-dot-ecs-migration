import pprint
import boto3
import json
from botocore.exceptions import ClientError

from src.utils import utils
from src.utils import awsutils
from src.ec2 import describe_instances


def create_roles(client, vars):
    with open('input/dest-roles.txt') as infile:
        dct = json.load(infile)

    dct_new_roles = {}
    for role_name, elt in dct.items():
        new_role_name = role_name.replace(vars['SourceRolePolicyPrefix'],
                                          vars['TargetRolePolicyPrefix'])

        try:
            res = client.create_role(RoleName=new_role_name,
                                     Description=elt['Description'],
                                     AssumeRolePolicyDocument=json.dumps(elt['AssumeRolePolicyDocument']))

            dct_new_roles[new_role_name] = elt

            pprint.pprint(dct_new_roles[new_role_name])

        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                pprint.pprint('WARNING: role already exists: ' + new_role_name)
            else:
                raise e

    return dct_new_roles


def main():
    vars = awsutils.read_vars()
    iam = boto3.client('iam')
    res = create_roles(iam, vars)

    with open('input/created-roles.txt', 'w') as outfile:
        outfile.write(json.dumps(res, indent=4))

    #pprint.pprint(json.dumps(res, indent=4))
    
    return res



if __name__ == '__main__':
    main()


