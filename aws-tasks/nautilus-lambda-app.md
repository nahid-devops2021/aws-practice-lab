# Nautilus Lambda CloudFormation Setup Guide

## Objective
Deploy AWS Lambda using CloudFormation.

## Stack Details
- Stack Name: nautilus-lambda-app
- Lambda Function: nautilus-lambda
- Runtime: Python (python3.12)
- IAM Role: lambda_execution_role
- Response: Welcome to KKE AWS Labs!
- Status Code: 200

## CloudFormation Template

Save as /root/nautilus-lambda.yml

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Lambda + IAM Role setup

Resources:

  lambda_execution_role:
    Type: AWS::IAM::Role
    Properties:
      RoleName: lambda_execution_role
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service:
                - lambda.amazonaws.com
            Action:
              - sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

  NautilusLambda:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: nautilus-lambda
      Runtime: python3.12
      Handler: index.lambda_handler
      Role: !GetAtt lambda_execution_role.Arn
      Timeout: 30
      Code:
        ZipFile: |
          def lambda_handler(event, context):
              return {
                  "statusCode": 200,
                  "body": "Welcome to KKE AWS Labs!"
              }
```

## Deploy

aws cloudformation create-stack \
  --stack-name nautilus-lambda-app \
  --template-body file:///root/nautilus-lambda.yml \
  --capabilities CAPABILITY_NAMED_IAM

## Wait

aws cloudformation wait stack-create-complete --stack-name nautilus-lambda-app

## Test

aws lambda invoke --function-name nautilus-lambda response.json
cat response.json
