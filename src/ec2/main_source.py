import logging
import pprint
import boto3
import json
import time
from botocore.exceptions import ClientError

from src.utils import awsutils
from src.ec2 import create_images
from src.ec2 import copy_images
from src.ec2 import share_images


create_images.main(waitForCompletion = True)
copy_images.main(waitForCompletion = True)
share_images.main()
