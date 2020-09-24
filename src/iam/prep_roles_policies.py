import pprint
import boto3
import json
from botocore.exceptions import ClientError

from src.utils import utils
from src.utils import awsutils


def prep_roles(roles):
    vars = awsutils.read_vars()
    src = vars['SourceAccount']
    dest = vars['TargetAccount']
    res = roles.replace(src, dest)
    return res


def prep_policies_NOT_FINISHED(policies):
    vars = awsutils.read_vars()
    srcPrefix = vars['SourceAccount']
    destPrefix = 'DELETE_ME'  # vars['TargetAccount']

    s3map = utils.map_s3_to_ecs_prod()

    dct = json.loads(policies)
    for policyName, policyElement in dct.items():
        destPolicyElement = policyElement
        destStatement = []
        for elt in policyElement['Document']['Statement']:
            resource = elt['Resource']

            if isinstance(resource, list):
                destResource = []
                for r in resource:
                    found = False
                    for srcS3, destS3 in s3map.items():
                        if srcS3 in r:
                            found = True
                            destResource.append(r.replace(srcS3, destS3))
                        #res = res.replace(k, v)
                        # TODO: cleanup non-existing resources
                        # will have to work with the actual structure

                elt = destResource



    return json.dumps(dct, indent=4)


def prep_policies(policies):
    s3map = utils.map_s3_to_ecs_prod()
    res = policies
    for k, v in s3map.items():
        res = res.replace(k, v)
        # TODO: cleanup non-existing resources
        # will have to work with the actual structure

    vars = awsutils.read_vars()
    src = vars['SourceAccount']
    dest = 'DELETE_ME'  # vars['TargetAccount']
    res = res.replace(src, dest)
    return res


def main():
    with open('input/src-policies.txt') as infile:
        policies = infile.read()

    with open('input/src-roles.txt') as infile:
        roles = infile.read()

    policies = prep_policies(policies)
    roles = prep_roles(roles)

    with open('input/dest-roles.txt', 'w') as outfile:
        outfile.write(roles)

    with open('input/dest-policies.txt', 'w') as outfile:
        outfile.write(policies)


if __name__ == '__main__':
    main()


