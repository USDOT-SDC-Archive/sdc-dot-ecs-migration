import logging
import pprint
import boto3
import json
import time
from botocore.exceptions import ClientError

import awsutils
import copy_target_images
import launch_target_instances


copy_target_images.main(waitForCompletion = True)
launch_target_instances.main()
