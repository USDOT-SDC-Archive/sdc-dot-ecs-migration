#!/bin/bash

. vars

echo mark=$MARK
echo env=$ENV_TAG
echo kms=$ENCRYPTION_KEY


#LANG=C aws $PROFILE ec2 describe-snapshots --filters "Name=tag:ECSMigrate,Values=$MARK" --filters 'Name=tag:MigrateState,Values=QuarantineEncrypted' --query 'Snapshots[*].{ID:SnapshotId,Description:Description}' --output text | sed 's/snap-/,snap-/g' | tr -s ' \t' ' ' | awk -F, -v env=$ENV_TAG -v mark=$MARK -v kms=$ENCRYPTION_KEY ' { printf "LANG=C aws ec2 copy-snapshot --encrypted --region us-east-1 --source-region us-east-1 --description \"%sECS Encryption\" --source-snapshot-id %s --kms-key-id alias/%s --tag-specifications \"ResourceType=snapshot,Tags=[{Key=ECSMigrate,Value=%s},{Key=Environment,Value=%s},{Key=MigrateState,Value=ECSEncrypted}]\"\n", $1, $2, kms, mark, env } ' > $COPY_CMD_FILE

LANG=C aws $PROFILE ec2 describe-snapshots --filters "Name=tag:ECSMigrate,Values=$MARK" "Name=tag:MigrateState,Values=QuarantineEncrypted" --query 'Snapshots[*].{ID:SnapshotId,Description:Description}' --output text | sed 's/snap-/,snap-/g' | tr -s ' \t' ' ' | awk -F, -v env=$ENV_TAG -v mark=$MARK -v kms=$ENCRYPTION_KEY ' { printf "LANG=C aws ec2 copy-snapshot --encrypted --region us-east-1 --source-region us-east-1 --description \"%sECS Encryption\" --source-snapshot-id %s --kms-key-id alias/%s --tag-specifications \"ResourceType=snapshot,Tags=[{Key=ECSMigrate,Value=%s},{Key=Environment,Value=%s},{Key=MigrateState,Value=ECSEncrypted}]\"\n", $1, $2, kms, mark, env } ' > $COPY_CMD_FILE

chmod +x $COPY_CMD_FILE

