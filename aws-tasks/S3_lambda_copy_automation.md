# AWS S3 → Lambda → DynamoDB Automation Guide (Console + CLI)

This guide explains how to build an automated file transfer system using **AWS Console and AWS CLI**.

---

# Architecture Overview

1. File uploaded to **Public S3 bucket**
2. **Lambda function** is triggered
3. File is copied to **Private S3 bucket**
4. Metadata is logged into **DynamoDB table**

---

# Prerequisites

- AWS account access
- IAM permissions for S3, Lambda, DynamoDB, IAM
- AWS CLI configured (`aws configure`)
- Files available:
  - `/root/sample.zip`
  - `/root/lambda-function.py`

---

# Step 1: Create S3 Buckets

## 1.1 Public S3 Bucket (datacenter-public-10840)

### ✔ CLI Method

```bash
aws s3 mb s3://datacenter-public-10840
```

Disable Block Public Access:

```bash
aws s3api put-public-access-block \
--bucket datacenter-public-10840 \
--public-access-block-configuration BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false
```

Create bucket policy (`public-policy.json`):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::datacenter-public-10840/*"
    }
  ]
}
```

Apply policy:

```bash
aws s3api put-bucket-policy \
--bucket datacenter-public-10840 \
--policy file://public-policy.json
```

---

### ✔ AWS Console Method

1. Go to **S3 Console**
2. Click **Create bucket**
3. Bucket name: `datacenter-public-10840`
4. Uncheck **Block all public access**
5. Confirm warning
6. Create bucket
7. Go to **Permissions → Bucket Policy**
8. Paste public-read policy

---

## 1.2 Private S3 Bucket (datacenter-private-16950)

### ✔ CLI Method

```bash
aws s3 mb s3://datacenter-private-16950
```

Enable strict private access:

```bash
aws s3api put-public-access-block \
--bucket datacenter-private-16950 \
--public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```

---

### ✔ Console Method

1. S3 Console → Create bucket
2. Name: `datacenter-private-16950`
3. Keep **Block all public access = ON**
4. Create bucket

---

# Step 2: Create DynamoDB Table

Table: `datacenter-S3CopyLogs`

Partition key: `LogID (String)`

## ✔ CLI Method

```bash
aws dynamodb create-table \
--table-name datacenter-S3CopyLogs \
--attribute-definitions AttributeName=LogID,AttributeType=S \
--key-schema AttributeName=LogID,KeyType=HASH \
--billing-mode PAY_PER_REQUEST
```

## ✔ Console Method

1. Open DynamoDB Console
2. Click **Create table**
3. Table name: `datacenter-S3CopyLogs`
4. Partition key: `LogID` (String)
5. Create table

---

# Step 3: Create IAM Role (lambda_execution_role)

## ✔ Console Method

1. Go to IAM → Roles → Create role
2. Trusted entity: Lambda
3. Attach policy:
   - AWSLambdaBasicExecutionRole
4. Create role: `lambda_execution_role`

Then attach inline policies:

### S3 Access Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": [
        "arn:aws:s3:::datacenter-public-10840/*",
        "arn:aws:s3:::datacenter-private-16950/*"
      ]
    }
  ]
}
```

### DynamoDB Access Policy

```json
{
  "Effect": "Allow",
  "Action": "dynamodb:PutItem",
  "Resource": "arn:aws:dynamodb:*:*:table/datacenter-S3CopyLogs"
}
```

---

## ✔ CLI Method

Trust policy (`trust-policy.json`):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }
  ]
}
```

```bash
aws iam create-role \
--role-name lambda_execution_role \
--assume-role-policy-document file://trust-policy.json
```

Attach basic execution policy:

```bash
aws iam attach-role-policy \
--role-name lambda_execution_role \
--policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

Add inline policies:

```bash
aws iam put-role-policy \
--role-name lambda_execution_role \
--policy-name S3Access \
--policy-document file://s3-policy.json
```

```bash
aws iam put-role-policy \
--role-name lambda_execution_role \
--policy-name DynamoDBAccess \
--policy-document file://ddb-policy.json
```

---

# Step 4: Update Lambda Code

Edit `/root/lambda-function.py`

Replace:

- `REPLACE-WITH-YOUR-DYNAMODB-TABLE` → `datacenter-S3CopyLogs`
- `REPLACE-WITH-YOUR-PRIVATE-BUCKET` → `datacenter-private-16950`

```python
DDB_TABLE = "datacenter-S3CopyLogs"
PRIVATE_BUCKET = "datacenter-private-16950"
```

---

# Step 5: Create Lambda Function

## ✔ CLI Method

```bash
cd /root
zip function.zip lambda-function.py
```

```bash
aws lambda create-function \
--function-name datacenter-copyfunction \
--runtime python3.9 \
--role arn:aws:iam::<ACCOUNT_ID>:role/lambda_execution_role \
--handler lambda-function.lambda_handler \
--zip-file fileb://function.zip
```

## ✔ Console Method

1. Go to Lambda Console
2. Click **Create function**
3. Name: `datacenter-copyfunction`
4. Runtime: Python 3.9
5. Role: Existing role → `lambda_execution_role`
6. Upload `/root/function.zip`
7. Create function

---

# Step 6: Add S3 Trigger

## ✔ Console Method

1. Open Lambda → datacenter-copyfunction
2. Click **Add trigger**
3. Select S3
4. Bucket: `datacenter-public-10840`
5. Event: All object create events
6. Add trigger

---

## ✔ CLI Method

```bash
aws lambda add-permission \
--function-name datacenter-copyfunction \
--statement-id s3invoke \
--action lambda:InvokeFunction \
--principal s3.amazonaws.com \
--source-arn arn:aws:s3:::datacenter-public-10840
```

```bash
aws s3api put-bucket-notification-configuration \
--bucket datacenter-public-10840 \
--notification-configuration '{
  "LambdaFunctionConfigurations": [
    {
      "LambdaFunctionArn": "arn:aws:lambda:<REGION>:<ACCOUNT_ID>:function:datacenter-copyfunction",
      "Events": ["s3:ObjectCreated:*"]
    }
  ]
}'
```

---

# Step 7: Test the Setup

## Upload file

```bash
aws s3 cp /root/sample.zip s3://datacenter-public-10840/
```

---

# Step 8: Verification

## Check private bucket

```bash
aws s3 ls s3://datacenter-private-16950/
```

## Check DynamoDB logs

```bash
aws dynamodb scan --table-name datacenter-S3CopyLogs
```

Expected fields:

- LogID
- SourceBucket
- DestinationBucket
- ObjectKey

---

# Summary

✔ Public S3 upload bucket
✔ Private secure S3 bucket
✔ Lambda auto-copy function
✔ DynamoDB logging system
✔ Console + CLI implementation

---

# End of Guide

