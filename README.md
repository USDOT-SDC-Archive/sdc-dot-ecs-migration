# sdc-dot-ecs-migration

# README Outline:
* Project Description
* Prerequisites
* Usage
	* Building
	* Testing
	* Execution
* Additional Notes
* Version History and Retention
* License
* Contributions
* Contact Information
* Acknowledgements

# Project Description

This repository contains tools and documentation to aid with migration of the Secure Data Commons resources from external Amazon Web Services (AWS) account to the USDOT Enterprise Cloud Services (ECS) environment.

# Prerequisites

Requires:
- aws cli version 2 or higher
- Python version 5.3 or higher
- Python boto3 library 

The preferred environment for execution is Linux - but will work in Windows as well if you have corresponding utilities installed.

# Usage

## Building
As this is Python-based code, there are no build requirements. 

## Testing
There are no unit tests at this time. Manual testing will need to be conducted for each specific workstation after migration.

## Execution
All source code files are located into the "src" folder. Follow the steps below after downloading the source code.

### Preparation

1. Create "input" folder under the "src" folder.
2. Create vars.txt file in the "src/input" folder. The file should define execution variables as follows:

```
{
    "InstancesInputFile": [json file with the list of instances to migrate],
    "EcsQuarantineCopiedPrefix": "prefix to add to the names of AMI images in the source account",
    "EcsSharedPrefix": [prefix to add to the names of AMI images to be shared with the target account],
    "EcsRestoredPrefix": [prefix for AMI images and EC2 instances to add to AMIs and EC2s restored in the target account],
    "SourceKmsKeyId": [source account KMS key, shared with the target account],
    "TargetKmsKeyId": [target account KMS key to use],
    "TargetAccount": [target AWS account number],
    "EC2KeyName": [target account key name for creating EC2 instances],
    "EC2SecurityGroupIds": [list of target account security groups to assign to EC2 instances],
    "EC2SubnetId": [target account subnet ID to place EC2 instances]
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
    "TargetAccount": "1234567890",
    "EC2KeyName": "target-account-ec2-creation-key",
    "EC2SecurityGroupIds": ["sg-1111", "sg-2222"],
    "EC2SubnetId": "subnet-123abc"
}
```


3. Create instances.txt file in the "src/input" folder. The file should contain json representation of a list of EC2 instances you want to migrate.

Example content:

```
[
    "i-1111",
    "i-2222",
    "i-3333",
    "i-4444"
]

```

### Execution with explanations

**From the source environment**

1. Run the following command to verify that all instances are stopped:

```
python describe_instances.py
```

2. Run the following command to create base AMIs for the desired instances to work with. This will create input/base_amis.txt file:

```
python create_images.py
```

3. Run the following command to create copies of AMIs. The AMIs will be encrypted with the KMS key that's shared with the target account. This command will create input/base_amis.txt file.

```
python copy_images.py
```

4. When the images are created (completed), run the following command to change their permissions and permissions of underlying snapshots to share with the target account:

```
python share_images.py
```

**In the target environment**
5. Download the repository, create "src/input" folder, copy over vars.txt and copied_images.txt

6. Run the following command to copy images locally (creates input/copied_target_amis.txt)

```
python copy_target_images.py
```

7. Run the following command to finally) launch instances in the target account:

```
python launch_target_instances.py
```


# Version History and Retention

**Status:** This project is in the release/active development phase.

**Release Frequency:** This project is updated as prioritized within the Secure Data Commons activities.

**Release History: See [CHANGELOG.md](CHANGELOG.md)**

**Retention:** This project will remain publicly accessible for a minimum of five years (until at least 06/15/2025).

# License
This project is licensed under the MIT License - see the [License.MD](https://github.com/usdot-jpo-sdc-projects/sdc-dot-ecs-migration/blob/master/LICENSE) for more details. 

# Contributions
Please read [CONTRIBUTING.md](https://github.com/usdot-jpo-sdc-projects/sdc-dot-ecs-migration/blob/master/Contributing.MD) for details on our Code of Conduct, the process for submitting pull requests to us, and how contributions will be released.

# Contact Information
Contact Name: USDOT ITS JPO Secure Data Commons
Contact Information: sdc-support@dot.gov

# Acknowledgements
To track how this government-funded code is used, we request that if you decide to build additional software using this code please acknowledge its Digital Object Identifier in your software's README/documentation.

Digital Object Identifier: (fill in with DOI)

Shout out to [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2) for their README template.
