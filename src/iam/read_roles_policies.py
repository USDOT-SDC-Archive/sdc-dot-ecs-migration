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

    dct_role_policies = {}
    dct_policies = {}

    for role in roles:
        #role_res = iam.get_role(RoleName = role)
        res = iam.list_attached_role_policies(RoleName = role)
        attached_policies = res['AttachedPolicies']
        dct_role_policies[role] = attached_policies

        for p in attached_policies:
            if not p['PolicyName'] in dct_policies.keys():
                res = iam.get_policy(PolicyArn=p['PolicyArn'])
                policy = res['Policy']

                res = iam.get_policy_version(
                   PolicyArn = policy['Arn'],
                   VersionId = policy['DefaultVersionId']
                )

                policy_version = res['PolicyVersion']
                doc = { 'Document': policy_version['Document'] }
                if 'Description' in policy.keys():
                    doc['Description'] = policy['Description']

                #policy_version['CreateDate'] = ''

                #pprint.pprint(policy_version)
                pprint.pprint(json.dumps(doc, indent=4))
                dct_policies[p['PolicyName']] = doc

    with open('input/src-roles.txt', 'w') as outfile:
        json.dump(dct_role_policies, outfile, indent=4)

    with open('input/src-policies.txt', 'w') as outfile:
        json.dump(dct_policies, outfile, indent=4)



if __name__ == '__main__':
    main()


