| Date | Author | Description | Version |
| --- | --- | --- | --- |
| 29/03/2018 | Wagner Alves (aka Barão) | Python Script | 1.0 | 

# create_or_update_stack
Python script for create or update RDS Cloud Formation stack.

## Before the execution:

> 1- In order to execute this script you will need to have AWS credentials set into <user>/.aws/credentials file, such as:

```
[default]
aws_access_key_id = AKIA...
aws_secret_access_key = FY0czy0x...
region = us-east-1

```
(OPTIONAL) If you have Role Based credentials configured into 'credentials' and 'config' files, you can get session token executing the 'aws-session-token.sh' shell script, such as:
```
. aws-session-token.sh <profile_from_config_file>
```
- WARNING: this script above depends on the NPM module 'aws-assume', and you can install typing:
```
npm install aws-assume -g
```

> 2- Make sure the AWS resources are set into 'rds-template.yml' file.

> 3- Set the necessary parameters into 'rds-parameters.json' file.

## How to execute:

On rds folder, on command line type:
```
python ../create_or_update_stack.py <stack_name> <stack_template> <parameters_file> <environment>

```

Example:
```
python ../create_or_update_stack.py MySQL-RDS-DB rds-template.yml rds-parameters.json dev

```

## I hoje you enjoy it! ;-)