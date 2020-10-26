import logging
import pprint
import boto3
import json
from src.utils import awsutils
from botocore.exceptions import ClientError
from src.ec2 import describe_instances

#logger = logging.getLogger(__name__)
#ec2 = boto3.resource('ec2')


def build_import(instances, instance_ips, full_tpl, node_tpl):
    res = ''
    nodes = ''
    for i, elt in instances.items():
        name = elt['Team'] + ' - ' + elt['OS'] + ' - ' + elt['Owner']
        description = elt['Team'] + ' - ' + elt['OS']
        ip = instance_ips[i]
        node = node_tpl.replace('$NAME', name).replace('$DESCRIPTION', description).replace('$IP', ip)
        nodes = nodes + node + '\n'
        #pprint.pprint(i + ' --> ' + json.dumps(elt, indent=4))
        pprint.pprint(node)

    res = full_tpl.replace('$NODES', nodes)

    return res

# main
def main():
    vars = awsutils.read_vars()
    client = awsutils.get_ec2_client('us-east-1')

    with open('templates/mng_node_tpl.xml') as infile:
        node_tpl = infile.read()

    with open('templates/mng_full_tpl.xml') as infile:
        full_tpl = infile.read()

    with open('../ec2/input/launched_target_ec2s.txt') as infile:
        lst = json.load(infile)

    instance_ids = []
    for i in lst:
        instance_ids.append(i[5])

    instances = describe_instances.get_instances(client, instance_ids)

    instance_ips = {}
    for i in instances:
        instance_ips[i['InstanceId']] = i['NetworkInterfaces'][0]['PrivateIpAddress']

    dct = describe_instances.repackage_instances_as_dct(instances)

    txt = build_import(dct, instance_ips, full_tpl, node_tpl)

    with open('input/BulkImport.xml', 'w') as outfile:
        outfile.write(txt)


    return instances


if __name__ == '__main__':
    main()

