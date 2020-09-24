import pprint
import boto3
import json
from botocore.exceptions import ClientError

from src.utils import utils
from src.utils import awsutils
from src.ec2 import describe_instances


def create_policies(client, vars):
    with open('input/dest-policies.txt') as infile:
        dct = json.load(infile)

    res_policies = {}
    for k, v in dct.items():
        # TODO: move this replacement into prep_roles_policies.py
        name = k.replace(vars['SourceRolePolicyPrefix'],
                         vars['TargetRolePolicyPrefix'])

        try:
            policyDocument = json.dumps(v['Document'])
            description = ''
            if 'Description' in v.keys():
                description = v['Description']

            #pprint.pprint(name + ' --> ' + description)
            res = client.create_policy(PolicyName=name,
                                       PolicyDocument=policyDocument,
                                       Description=description)

            res_policies[name] = res['Policy']
            pprint.pprint(res['Policy'])

        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                pprint.pprint('WARNING: policy already exists: ' + name)
            else:
                raise e

    return res_policies


def main():
    vars = awsutils.read_vars()
    iam = boto3.client('iam')
    res = create_policies(iam, vars)


if __name__ == '__main__':
    main()


