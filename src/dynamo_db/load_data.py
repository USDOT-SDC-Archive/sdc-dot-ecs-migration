import pprint
import boto3
import json
from botocore.exceptions import ClientError

from src.utils import awsutils


def map_s3_to_ecs_prod():
    with open('input/s3-map-raw.txt') as f:
        lines = f.read().splitlines()

    dct = {}
    for kv in lines:
        k = kv.split()[0]
        v = kv.split()[1]

        dct[k] = v

    return dct


def map_ec2_to_ecs_prod():
    with open('input/dynamo_target_ec2s.txt') as infile:
        lst = json.load(infile)

    dct = {}
    for elt in lst:
        k = elt[0]
        v = elt[5]

        dct[k] = v

    return dct


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
    vars = awsutils.read_vars()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(vars['DynamoDBDestinationStacks'])

    with open('input/dest-user-stacks.txt') as infile:
        users = json.load(infile)

    for k, v in users.items():
        resp = table.get_item(Key={'username': k })

        # only write those that dont exist
        if not 'Item' in resp.keys():
            table.put_item(Item = v)
            pprint.pprint(json.dumps(resp, indent=4))

    #pprint.pprint(json.dumps(dest_users, indent=4))
    return users


if __name__ == '__main__':
    main()


