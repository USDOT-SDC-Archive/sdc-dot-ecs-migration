import logging
import pprint
import boto3
import json
import time
from botocore.exceptions import ClientError

from src.utils import awsutils
from src.iam import read_roles_policies
from src.iam import prep_roles_policies


read_roles_policies.main()
prep_roles_policies.main()
