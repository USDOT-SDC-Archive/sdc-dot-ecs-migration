import pprint
import boto3
import json
from botocore.exceptions import ClientError

from src.utils import utils
from src.utils import awsutils


def main():
    vars = awsutils.read_vars()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(vars['DynamoDBRequestExportTable'])

    items = table.scan()['Items']
    #pprint.pprint(items)

    # this repackaging is needed because of a decimal inside:
    # cannot dump json otherwise
    out = []
    for i in items:
        i['ReqReceivedTimestamp'] = str(i['ReqReceivedTimestamp'])
        out.append(i)

    with open('input/src-request-export.txt', 'w') as f:
        f.write(json.dumps(out, indent=4))

    #pprint.pprint(json.dumps(out, indent=4))
    return out


if __name__ == '__main__':
    main()


