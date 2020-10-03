import pprint
import boto3
import json
from botocore.exceptions import ClientError

from src.utils import utils


def main():
    s3map = utils.map_s3_to_ecs_prod()

    with open('input/src-request-export.txt') as infile:
        exports = infile.read()

    for k, v in s3map.items():
        exports = exports.replace(k, v)

    with open('input/dest-request-exports.txt', 'w') as outfile:
        outfile.write(exports)

    return exports


if __name__ == '__main__':
    main()


