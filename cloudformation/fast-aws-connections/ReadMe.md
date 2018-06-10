| Date | Author | Description | Version |
| --- | --- | --- | --- |
| 29/03/2018 | Wagner Alves (aka Barão) | Python Script | 1.0 | 

# create_or_update_stack
Python script for create or update Cloud Formation stack.

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

> 2- Make sure the AWS resources are set into 'fac-template.yml' file.

```
AWSTemplateFormatVersion: '2010-09-09'
Parameters:
  QueueName:
    Type: String
  ReceiveMessageWaitTimeSeconds:
    Type: Number
  VisibilityTimeout:
    Type: Number
  MaximumMessageSize:
    Type: Number
    ...  
Resources:
  FastAWSConnetionsQueue:
    Type: "AWS::SQS::Queue"
    Properties:
      QueueName: Fast-AWS-Connections-Queue
    ...
```

> 3- Set the necessary parameters into 'parameters.json' file.

```
[
    {
        "ParameterKey": "QueueName",
        "ParameterValue": "Fast-AWS-Connections-Queue"
    },
    {
        "ParameterKey": "ReceiveMessageWaitTimeSeconds",
        "ParameterValue": "0"
    },
    {
        "ParameterKey": "VisibilityTimeout",
        "ParameterValue": "30"
    },
    {
        "ParameterKey": "MaximumMessageSize",
        "ParameterValue": "262144"
    },
    {
        "ParameterKey": "MessageRetentionPeriod",
        "ParameterValue": "345600"
    },
    {
        "ParameterKey": "DelaySeconds",
        "ParameterValue": "0"
    }
]
```


## How to execute:

Into folder 'fast-aws-connections', on command line type:
```
python ../create_or_update_stack.py <stack_name> <stack_template> <parameters_file> <environment>

```

Example:
```
python ../create_or_update_stack.py FastAWSConnectionsTeste fac-template.yml parameters.json dev

```

## I hoje you enjoy it! ;-)