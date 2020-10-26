#!/bin/bash

. vars

echo mark=$MARK
echo env=$ENV_TAG
echo kms=$ENCRYPTION_KEY
echo target_acct=$TARGET_ACCT

for i in `LANG=C aws ec2 describe-snapshots --filters "Name=tag:ECSMigrate,Values=$MARK" "Name=tag:MigrateState,Values=ECSEncrypted" --query 'Snapshots[*].{ID:SnapshotId}' --output text`; do LANG=C aws ec2 modify-snapshot-attribute --snapshot-id $i --attribute createVolumePermission --operation add --user-ids $TARGET_ACCT ; done


