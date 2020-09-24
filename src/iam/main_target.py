import logging
import pprint
import boto3
import json
import time
from botocore.exceptions import ClientError

from src.utils import awsutils
from src.iam import create_policies
from src.iam import create_roles
from src.iam import attach_role_policies
from src.ec2 import attach_roles_to_ec2s


create_policies.main()
create_roles.main()
attach_role_policies.main()
attach_roles_to_ec2s.main()
