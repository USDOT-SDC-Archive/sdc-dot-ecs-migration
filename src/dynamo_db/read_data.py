import pprint
import boto3
import json
from botocore.exceptions import ClientError

def get_src_users_instances_map():
    with open('input/src-users-instances-raw.txt') as f:
        lines = f.read().splitlines()

    dct = {}
    for kv in lines:
        k = kv.split()[0]
        v = kv.split()[1]

        if k in dct.keys():
            dct[k].append(v)
        else:
            dct[k] = [ v ]

    with open('input/src-users-instances-to-migrate.txt', 'w') as f:
        f.write(json.dumps(dct, indent=4))

    return dct


def map_s3_to_ecs_prod():
    with open('input/s3-map-raw.txt') as f:
        lines = f.read().splitlines()

    dct = {}
    for kv in lines:
        k = kv.split()[0]
        v = kv.split()[1]

        dct[k] = v

    return dct


def prep_user_for_ecs(usr, s3map):
    stacks = usr['stacks']
    for stack in stacks:
        team_bucket = stack['team_bucket_name']
        if team_bucket in s3map.keys():
            stack['team_bucket_name'] = s3map[team_bucket]

    return usr


def main():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('prod-UserStacksTable')

    dct = get_src_users_instances_map()

    users_res = {}
    for k, v in dct.items():
        usr_resp = table.get_item(Key={'username': k })
        users_res[k] = usr_resp['Item']

    with open('input/src-user-stacks.txt', 'w') as f:
        f.write(json.dumps(users_res, indent=4))

    pprint.pprint(json.dumps(users_res, indent=4))
    #return response['Item']


if __name__ == '__main__':
    main()


