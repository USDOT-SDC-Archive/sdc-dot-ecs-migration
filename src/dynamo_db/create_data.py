import pprint
import boto3
import json
from botocore.exceptions import ClientError

from src.utils import awsutils


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


