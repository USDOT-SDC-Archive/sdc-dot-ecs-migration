import logging
import pprint
import boto3
import json
from src.utils import awsutils
from src.utils import utils
from botocore.exceptions import ClientError

#logger = logging.getLogger(__name__)
#ec2 = boto3.resource('ec2')


# main
def main():
    instances = utils.get_src_instances()

    with open('input/instances.txt', 'w') as outfile:
        json.dump(instances, outfile, indent=4)

    return instances


if __name__ == '__main__':
    main()

