# sdc-dot-ecs-migration

# README Outline:
* [Project Description](#project_description)
* [Prerequisites](#prerequisites)
* [Usage](#usage)
	* [Building](#usage_building)
	* [Testing](#usage_testing)
	* [Execution](#usage_execution)
* [Additional Notes](#additional_notes)
* [Version History and Retention](#version_history)
* [License](#license)
* [Contributions](#contributions)
* [Contact Information](#contact_information)
* [Acknowledgements](#acknowledgements)

<a name="project_description"/>

# Project Description

This repository contains tools and documentation to aid with migration of the Secure Data Commons resources from external Amazon Web Services (AWS) account to the USDOT Enterprise Cloud Services (ECS) environment.

<a name="prerequisites"/>

# Prerequisites

Requires:
- aws cli version 2 or higher
- Python version 3.5 or higher
- Python boto3 library 

Clone this repository twice: once for the source environment work and second time for the target environment work. Create "input" folders under each subfolder. Check .gitignore - those are the ones.

<a name="usage"/>

# Usage

<a name="usage_building"/>

## Building
As this is Python-based code, there are no build requirements. 

<a name="usage_testing"/>

## Testing
There are no unit tests at this time. Manual testing will need to be conducted for each specific workstation after migration.

<a name="usage_execution"/>

## Execution
All source code files are located into the "src" folder. Follow the steps below after downloading the source code.

### Preparation

1. Create "src/input" folder..
2. Create vars.txt file in the "src/input" folder. The file should define execution variables as follows:

```
{
    "InstancesInputFile": [json file with the list of instances to migrate],
    "EcsQuarantineCopiedPrefix": "prefix to add to the names of AMI images in the source account",
    "EcsSharedPrefix": [prefix to add to the names of AMI images to be shared with the target account],
    "EcsRestoredPrefix": [prefix for AMI images and EC2 instances to add to AMIs and EC2s restored in the target account],
    "SourceKmsKeyId": [source account KMS key, shared with the target account],
    "TargetKmsKeyId": [target account KMS key to use],
    "SourceAccount": [source AWS account nummber],
    "TargetAccount": [target AWS account number],
    "EC2KeyName": [target account key name for creating EC2 instances],
    "EC2SecurityGroupIds": [list of target account security groups to assign to EC2 instances],
    "EC2SubnetId": [target account subnet ID to place EC2 instances],
    "DynamoDBSourceStacks": [source account user stacks DynamoDB table name],
    "DynamoDBDestinationStacks": [target account user stacks DynamoDB table name],
    "SourceRolePolicyPrefix": [prefix of IAM policies and roles in the source account],
    "TargetRolePolicyPrefix": [prefix in the target account. will replace source prefix when creating roles and policies]
    
}
```
For example:
```
{
    "InstancesInputFile": "instances.txt",
    "EcsQuarantineCopiedPrefix": "QUARANTINE ",
    "EcsSharedPrefix": "SHARED ",
    "EcsRestoredPrefix": "ECS_RESTORED ",
    "SourceKmsKeyId": "alias/source-account-kms",
    "TargetKmsKeyId": "alias/target-account-kms",
    "SourceAccount": "1234567890",
    "TargetAccount": "1234567899",
    "EC2KeyName": "target-account-ec2-creation-key",
    "EC2SecurityGroupIds": ["sg-1111", "sg-2222"],
    "EC2SubnetId": "subnet-123abc",
    "DynamoDBSourceStacks": "prod-user-stacks-table",
    "DynamoDBDestinationStacks": "dev-user-stacks-table",
    "SourceRolePolicyPrefix": "prod-",
    "TargetRolePolicyPrefix": "dev-"

}
```

3. Create "src/ec2/input" folder. Files in this folder will assist with AMI sharing and EC2 instance re-creation in the destination AWS account.
4. Create instances.txt file in the "src/ec2/input" folder. The file should contain json representation of a list of EC2 instances you want to migrate.

Example content:

```
[
    "i-1111",
    "i-2222",
    "i-3333",
    "i-4444"
]

```

4. Create "src/dynamo_db/input" folder. Files in this folder will be used for user stacks table generation. Also, will be used in IAM policy and role migration.
5. Create "src/dynamo_db/input/s3-map-raw.txt" file. The file should contain mapping of source s3 bucket names to destination s3 bucket names. Each entry on a single line spearated by space. This list exists as a table in Confluence.

Example:

```
src-bucket-foo-111 dest-bucket-foo-222
src-bucket-bar-111 dest-bucket-bar-222
src-bucket-ree-111 dest-bucket-ree-222

```

6. Create "src/dynamo_db/input/src-users-instances-raw.txt" file to contain user to source instance mapping, space-separated on a single line. Same user may have multiple entries.

Example:

```
john i-111
john i-222
garry i-333
susie i-444

```
Note: in the future, this will be the main file to define instances to migrate and the file from step 4 will be auto-generated, so if these instructions are out of date make sure you don't spend time creating the step 4 file unnecessarily. Though no harm in doing so.


### Execution with explanations

WARNING: all execution has been done from PyCharm environment. There may be some inconsistencies if running from a command line.

#### EC2 instance automated migration

1. **In the source environment:** Run the following command to verify that all instances are stopped:

```
python describe_instances.py
```

2. **In the source environment:** Run the following command to duplicate and share base AMIs with the target account:

```
python src/ec2/main_source.py
```
Note: this is a long-running process. It does provide rudimentory progress updates.

3. The previous command will auto-generate src/ec2/input/copied_amis.txt file. Transfer it into the same location under the **target** environment.

4. **In the target environment:** Run the following command to create EC2 instances. This is also long-running:

```
python src/ec2/main_target.py
```

Note: at this point your instances should exist in the target environment. Outstanding: DynamoDB stack table migration and IAM polocies and roles migration.

4. The previous command will auto-generate src/ec2/input/launched_target_ec2s.txt file. Transfer it into the same location under the **source** environment. Also, create src/dynamo_db/input/dynamo_target_ec2s.txt file in the **source** environment and copy/paste content of launched_target_ec2s.txt into that new file as well.

5. **In the source environment:** execute these commands:

```
python src/dynamo_db/read_data.py
python src/dynamo_db/prep_data.py
```

6. This will generate src/dynamo_db/input/dest-user-stacks.txt. Copy this file into the same location in the **target** environment.

7. **In the target environment:** make sure DynamoDB stacks table exists. Execute

```
python src/dynamo_db/create_data.py
```

After this, DynamoDB user stacks table should be populated. Now it's just policies and roles for EC2 instances.

8. **In the source environment:** Execute

```
python src/iam/main_source.py
```

9. This will generate src/iam/input/dest-policies.txt and dest-roles.txt. Copy these files into the same location in the **target** environment.

10. **In the target environment:** Execute

```
python src/iam/main_target.py
```

As a result of this execution, all corresponding policies and roles will be created and attached to migrated instances.

#### Configuration in the target environment

Automation is in progress, but some steps will remain manual.

**Everything below is for target environment only.

##### Generate mRemoteNG import file for new instances

1. Execute the command below. It will generate a BulkImport.xml file in the src/domain/input folder, which can be imported by mRemoteNG manager. src/domain/input folder should exist prior to execution.

```
python src/domain/prep_mng_import.py
```

Here's the outline of what remains after automated migration:

- Fix local admin password expiration
- fix network/domains
- Add original User to Administrators group
- Run this script on migrated Windows machines: C:\ProgramData\Amazon\EC2-Windows\Launch\Scripts\InitializeInstance.ps1
- Add workstations to guacamole in guacamole settings
- Create guacamole users to map AD - make sure to allow both machines AND groups
- USER PROFILES (copy folders from orig to new user folders)
- Confirm SQL Workbench connects to Hadoop
- Disable clipboard on machines
--- https://automationadmin.com/2016/05/gpo-disable-clipboard-in-rdp/


- for SQL Server machine: re-add new users.

- for linux - fix hostname (
Jupyter:
- /etc/dhcpd.conf/dhclient.conf
- fix hostname
--- Amazon Linux v1: hostname: /etc/sysconfig/network
- fixDNSresolution
--- add itself to hosts file
--- something manual by Robert on DNS server to allow name resolution for new machines
------ opening a ticket with Amazon to learn why not self-registering


<a name="version_history"/>

# Version History and Retention

**Status:** This project is in the release/active development phase.

**Release Frequency:** This project is updated as prioritized within the Secure Data Commons activities.

**Release History: See [CHANGELOG.md](CHANGELOG.md)**

**Retention:** This project will remain publicly accessible for a minimum of five years (until at least 06/15/2025).

<a name="license"/>

# License
This project is licensed under the MIT License - see the [License.MD](https://github.com/usdot-jpo-sdc-projects/sdc-dot-ecs-migration/blob/master/LICENSE) for more details. 

<a name="contributions"/>

# Contributions
Please read [CONTRIBUTING.md](https://github.com/usdot-jpo-sdc-projects/sdc-dot-ecs-migration/blob/master/Contributing.MD) for details on our Code of Conduct, the process for submitting pull requests to us, and how contributions will be released.

<a name="contact_information"/>

# Contact Information
Contact Name: USDOT ITS JPO Secure Data Commons
Contact Information: sdc-support@dot.gov

<a name="acknowledgments"/>

# Acknowledgements
To track how this government-funded code is used, we request that if you decide to build additional software using this code please acknowledge its Digital Object Identifier in your software's README/documentation.

Digital Object Identifier: (fill in with DOI)

Shout out to [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2) for their README template.
