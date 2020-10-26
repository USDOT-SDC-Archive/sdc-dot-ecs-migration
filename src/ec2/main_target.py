import logging
import pprint
import boto3
import json
import time
from botocore.exceptions import ClientError

from src.utils import awsutils
from src.ec2 import copy_target_images
from src.ec2 import launch_target_instances


copy_target_images.main(waitForCompletion = True)
launch_target_instances.main()
