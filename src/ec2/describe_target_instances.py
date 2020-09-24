import logging
import pprint
import boto3
import json
from src.utils import awsutils
from botocore.exceptions import ClientError
from src.ec2 import describe_instances

#logger = logging.getLogger(__name__)
#ec2 = boto3.resource('ec2')


# main
def main():
    vars = awsutils.read_vars()
    client = awsutils.get_ec2_client('us-east-1')

    with open('input/launched_target_ec2s.txt') as infile:
        lst = json.load(infile)

    instance_ids = []
    for i in lst:
        instance_ids.append(i[5])

    instances = describe_instances.get_instances(client, instance_ids)

    for i in instances:
        pprint.pprint(i['NetworkInterfaces'][0]['PrivateIpAddress'])

    #pprint.pprint(instances)

    return instances


if __name__ == '__main__':
    main()

