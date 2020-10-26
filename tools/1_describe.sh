#!/bin/bash

#aws --profile sdc ec2 describe-instances --filters 'Name=tag:Name,Values=prod-hadoop-dw-cluster*' --query 'Reservations[*].Instances[*].[Tags[?Key==`Name`]|[0].Value,InstanceId,BlockDeviceMappings[*].Ebs.VolumeId]' --output json

#aws ec2 describe-instances --filters 'Name=tag:Name,Values=*v-hadoop-dev*' --query 'Reservations[*].Instances[*].[Tags[?Key==`Name`]|[0].Value,InstanceId,BlockDeviceMappings[*].Ebs.VolumeId]' --output json

#aws ec2 describe-instances --filters 'Name=tag:Name,Values=*v-hadoop-dev*' --query 'Reservations[*].Instances[*].[Tags[?Key==`Name`]|[0].Value,InstanceId,BlockDeviceMappings[0].Ebs.VolumeId,BlockDeviceMappings[1].Ebs.VolumeId,BlockDeviceMappings[2].Ebs.VolumeId]' --output text

#aws ec2 describe-instances --filters 'Name=tag:Name,Values=*v-hadoop-dev*' --query 'Reservations[*].Instances[*].[Tags[?Key==`Name`]|[0].Value,InstanceId]' --output table

aws ec2 describe-instances --filters 'Name=tag:Name,Values=*v-hadoop-dev*' --query 'Reservations[*].Instances[*].[Tags[?Key==`Name`]|[0].Value,InstanceId,BlockDeviceMappings[0].Ebs.VolumeId]' --output text


