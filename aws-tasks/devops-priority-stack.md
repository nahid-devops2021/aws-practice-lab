# AWS Priority Queuing Using SNS, SQS, Lambda and CloudFormation

## Objective
Implement a priority-based message processing system using SNS, SQS, and Lambda.

## Resources
- SNS Topic: devops-Priority-Queues-Topic
- SQS Queues:
  - devops-High-Priority-Queue
  - devops-Low-Priority-Queue
- Lambda Function: devops-priorities-queue-function
- IAM Role: lambda_execution_role
- Stack: devops-priority-stack

## Architecture
SNS Topic routes messages based on message attribute `priority`:
- high → High Priority Queue
- low → Low Priority Queue

Both queues trigger a Lambda function via event source mapping.

## Deployment Steps

### 1. Create Stack
```bash
aws cloudformation create-stack   --stack-name devops-priority-stack   --template-body file:///root/devops-priority-stack.yml   --capabilities CAPABILITY_NAMED_IAM
```

Wait:
```bash
aws cloudformation wait stack-create-complete   --stack-name devops-priority-stack
```

### 2. Package Lambda Code
```bash
cd /root
zip function.zip index.py
```

### 3. Update Lambda Code
```bash
aws lambda update-function-code   --function-name devops-priorities-queue-function   --zip-file fileb://function.zip
```

## Testing

Get topic ARN:
```bash
topicarn=$(aws sns list-topics --query "Topics[?contains(TopicArn, 'devops-Priority-Queues-Topic')].TopicArn" --output text)
```

Publish messages:
```bash
aws sns publish --topic-arn $topicarn --message "High Priority message 1" --message-attributes '{"priority":{"DataType":"String","StringValue":"high"}}'

aws sns publish --topic-arn $topicarn --message "High Priority message 2" --message-attributes '{"priority":{"DataType":"String","StringValue":"high"}}'

aws sns publish --topic-arn $topicarn --message "Low Priority message 1" --message-attributes '{"priority":{"DataType":"String","StringValue":"low"}}'

aws sns publish --topic-arn $topicarn --message "Low Priority message 2" --message-attributes '{"priority":{"DataType":"String","StringValue":"low"}}'
```

## Verification
Check logs:
```bash
aws logs tail /aws/lambda/devops-priorities-queue-function --follow
```

Expected order:
- High Priority messages processed first
- Low Priority messages processed later
