#!/bin/bash

. vars

echo $ENV_TAG

cat ${VOLUMES_FILE} | sed 's/ /-/g' | sed "s/\t/${TOKEN_SEP}/g" | awk -F${TOKEN_SEP} -v env=$ENV_TAG -v mark=$MARK ' { printf "LANG=C aws ec2 create-snapshots --instance-specification InstanceId=%s --description \"ECS Migration Snapshot %s\" --tag-specifications \"ResourceType=snapshot,Tags=[{Key=ECSMigrate,Value=%s},{Key=Environment,Value=%s},{Key=MigrateState,Value=QuarantineEncrypted},{Key=InstanceId,Value=%s}]\"\n", $2, $1, mark, env, $2 } '  > ${CREATE_CMD_FILE}

chmod +x ${CREATE_CMD_FILE}

