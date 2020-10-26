import logging
import pprint
import boto3
import json
from src.utils import awsutils
from botocore.exceptions import ClientError

#logger = logging.getLogger(__name__)
#ec2 = boto3.resource('ec2')

def list_roles():
    instances = main()

    for i in instances:
        tags = awsutils.get_instance_tags(i)
        s = i["IamInstanceProfile"]["Arn"].rpartition('/')[-1]
        pprint.pprint(s)

    return instances


def create_profiles(ec2client, iam_client, instances_roles):

    for instance_id, role_name in instances_roles.items():
        # 1: create profile
        try:
            res = iam_client.create_instance_profile(InstanceProfileName=instance_id)
            pprint.pprint(res)

        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                pprint.pprint('WARNING: profile already exists: ' + instance_id)
            else:
                raise e

    return instances_roles


def attach_roles_to_profiles(ec2client, iam_client, instances_roles):

    for instance_id, role_name in instances_roles.items():
        # 2: add a role
        try:
            res = iam_client.add_role_to_instance_profile(InstanceProfileName=instance_id,
                                                      RoleName=role_name)
            pprint.pprint(res)

        except ClientError as e:
            if e.response['Error']['Code'] == 'LimitExceeded':
                pprint.pprint('WARNING: profile with role already exists: ' + instance_id + " --> " + role_name)
            else:
                raise e

    return instances_roles


def attach_profiles_to_ec2s(ec2client, iam_client, instances_roles):

    all = {}
    for instance_id, role_name in instances_roles.items():
        # 3: attach profile to instance
        try:
            res = iam_client.get_instance_profile(InstanceProfileName=instance_id)

            res_profile = res['InstanceProfile']

            profile = {'Arn': res_profile['Arn'], 'Name': res_profile['InstanceProfileName']}
            res = ec2client.associate_iam_instance_profile(IamInstanceProfile=profile,
                                                           InstanceId=instance_id)

            pprint.pprint(res_profile)
            all[instance_id] = res_profile

        except ClientError as e:
            if e.response['Error']['Code'] == 'IncorrectState':
                pprint.pprint('WARNING: profile already attached: ' + instance_id + " --> " + role_name)
            else:
                raise e

    return all


# main
def main():
    vars = awsutils.read_vars()
    ec2client = awsutils.get_ec2_client('us-east-1')
    iam_client = boto3.client('iam')

    with open('input/launched_target_ec2s.txt') as infile:
        lst = json.load(infile)

    instance_roles = {}
    for i in lst:
        instance_roles[i[5]] = i[1]['IamRole']

    res = create_profiles(ec2client, iam_client, instance_roles)
    res = attach_roles_to_profiles(ec2client, iam_client, instance_roles)
    res = attach_profiles_to_ec2s(ec2client, iam_client, instance_roles)

    # pprint.pprint(instances)

    return res


if __name__ == '__main__':
    main()

