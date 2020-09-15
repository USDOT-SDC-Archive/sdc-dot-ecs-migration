import logging
import pprint
import boto3
import json
import time
from botocore.exceptions import ClientError

import awsutils
import create_images
import copy_images
import share_images


create_images.main(waitForCompletion = True)
copy_images.main(waitForCompletion = True)
share_images.main()
