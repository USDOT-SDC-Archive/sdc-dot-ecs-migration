import pprint
import boto3
import json
from botocore.exceptions import ClientError

from src.utils import utils


def prep_user_for_ecs(usr, s3map, ec2map):
    stacks = usr['stacks']

    dest_stacks = []
    for stack in stacks:
        src_instance_id = stack['instance_id']

        if src_instance_id in ec2map.keys():
            stack['instance_id'] = ec2map[src_instance_id]
            src_team_bucket = stack['team_bucket_name']
            if src_team_bucket in s3map.keys():
                stack['team_bucket_name'] = s3map[src_team_bucket]

            dest_stacks.append(stack)

    # this will ensure that instances not marked for migration are excluded
    usr['stacks'] = dest_stacks

    return usr


def main():
    s3map = utils.map_s3_to_ecs_prod()
    ec2map = utils.map_ec2_to_ecs_prod()
    #ec2map = utils.map_ec2_to_ecs_prod_simple()

    with open('input/src-user-stacks.txt') as infile:
        src_users = json.load(infile)

    dest_users = {}
    for k, v in src_users.items():
        usr = prep_user_for_ecs(v, s3map, ec2map)
        if len(usr['stacks']) > 0:
            dest_users[k] = usr

    with open('input/dest-user-stacks.txt', 'w') as outfile:
        json.dump(dest_users, outfile, indent=4)

    pprint.pprint(json.dumps(dest_users, indent=4))
    return dest_users


if __name__ == '__main__':
    main()


