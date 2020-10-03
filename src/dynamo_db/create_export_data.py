import pprint
import boto3
import json
import decimal
from botocore.exceptions import ClientError

from src.utils import awsutils


def main():
    vars = awsutils.read_vars()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(vars['DynamoDBRequestExportTable'])

    with open('input/dest-request-exports.txt') as infile:
        items = json.load(infile)

    for i in items:
        i['ReqReceivedTimestamp'] = dec = decimal.Decimal(i['ReqReceivedTimestamp'])
        pprint.pprint(i)
        table.put_item(Item = i)

    #pprint.pprint(json.dumps(dest_users, indent=4))
    return items


if __name__ == '__main__':
    main()


