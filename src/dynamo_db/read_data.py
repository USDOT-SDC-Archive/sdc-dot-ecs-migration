import pprint
import boto3
import json
from botocore.exceptions import ClientError

from src.utils import utils
from src.utils import awsutils


def main():
    vars = awsutils.read_vars()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(vars['DynamoDBSourceStacks'])

    dct = utils.get_src_users_instances_map()

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


