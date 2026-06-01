# devops-priority-stack.yml
AWSTemplateFormatVersion: '2010-09-09'
Description: >
  devops Priority Queuing System using Amazon SQS, SNS, and Lambda.
  Uses only AWS managed policies.

Resources:
  # IAM Role
  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: lambda_execution_role
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
        - arn:aws:iam::aws:policy/AmazonSQSFullAccess
        - arn:aws:iam::aws:policy/AmazonSNSFullAccess

  # SQS Queues
  devopsHighPriorityQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: devops-High-Priority-Queue
      VisibilityTimeout: 30
      MessageRetentionPeriod: 86400

  devopsLowPriorityQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: devops-Low-Priority-Queue
      VisibilityTimeout: 30
      MessageRetentionPeriod: 86400

  # SQS Queue Policies
  devopsHighPriorityQueuePolicy:
    Type: AWS::SQS::QueuePolicy
    Properties:
      Queues:
        - !Ref devopsHighPriorityQueue
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: sns.amazonaws.com
            Action: sqs:SendMessage
            Resource: !GetAtt devopsHighPriorityQueue.Arn
            Condition:
              ArnEquals:
                aws:SourceArn: !Ref devopsPriorityQueuesTopic

  devopsLowPriorityQueuePolicy:
    Type: AWS::SQS::QueuePolicy
    Properties:
      Queues:
        - !Ref devopsLowPriorityQueue
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: sns.amazonaws.com
            Action: sqs:SendMessage
            Resource: !GetAtt devopsLowPriorityQueue.Arn
            Condition:
              ArnEquals:
                aws:SourceArn: !Ref devopsPriorityQueuesTopic

  # SNS Topic
  devopsPriorityQueuesTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: devops-Priority-Queues-Topic

  # SNS Subscriptions (with Filters)
  HighPrioritySubscription:
    Type: AWS::SNS::Subscription
    Properties:
      TopicArn: !Ref devopsPriorityQueuesTopic
      Protocol: sqs
      Endpoint: !GetAtt devopsHighPriorityQueue.Arn
      FilterPolicy:
        priority:
          - high

  LowPrioritySubscription:
    Type: AWS::SNS::Subscription
    Properties:
      TopicArn: !Ref devopsPriorityQueuesTopic
      Protocol: sqs
      Endpoint: !GetAtt devopsLowPriorityQueue.Arn
      FilterPolicy:
        priority:
          - low

  # Lambda Function
  devopsPrioritiesQueueFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: devops-priorities-queue-function
      Runtime: python3.12
      Handler: index.lambda_handler
      Role: !GetAtt LambdaExecutionRole.Arn
      Timeout: 60
      MemorySize: 128
      Environment:
        Variables:
          high_priority_queue: !Ref devopsHighPriorityQueue
          low_priority_queue: !Ref devopsLowPriorityQueue
      Code:
        ZipFile: |
          import boto3
          import os
          sqs = boto3.client('sqs')
          def delete_message(queue_url, receipt_handle, message):
              response = sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
              return "Message " + "'" + message + "'" + " deleted"

          def poll_messages(queue_url):
              QueueUrl=queue_url
              response = sqs.receive_message(
                  QueueUrl=QueueUrl,
                  AttributeNames=[],
                  MaxNumberOfMessages=1,
                  MessageAttributeNames=['All'],
                  WaitTimeSeconds=3
              )
              if "Messages" in response:
                  receipt_handle=response['Messages'][0]['ReceiptHandle']
                  message = response['Messages'][0]['Body']
                  delete_response = delete_message(QueueUrl,receipt_handle,message)
                  return delete_response
              else:
                  return "No more messages to poll"

          def lambda_handler(event, context):
              response = poll_messages(os.environ['high_priority_queue'])
              if response == "No more messages to poll":
                  response = poll_messages(os.environ['low_priority_queue'])
              return response
