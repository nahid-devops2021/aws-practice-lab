# AWS Lambda Deployment Runbook - devops-lambda

## Objective

Deploy a simple AWS Lambda function as part of the Nautilus DevOps initiative to demonstrate serverless capabilities.

The function will return a greeting message with HTTP status code 200.

---

## Requirements

- **Lambda Function Name:** devops-lambda
- **Runtime:** Python 3.x
- **Response Body:** `Welcome to KKE AWS Labs!`
- **Status Code:** 200
- **IAM Role:** lambda_execution_role

---

## Prerequisites

- AWS Console access
- IAM permissions for Lambda and IAM Role creation
- Access to AWS Management Console

---

# Step 1: Create IAM Role

## 1. Open IAM Console

- Go to AWS Management Console
- Search and open **IAM** service

## 2. Create Role

- Navigate to **Roles** → Click **Create role**

## 3. Select Trusted Entity

- Trusted entity type: **AWS service**
- Use case: **Lambda**

Click **Next**

## 4. Attach Permissions

Attach policy:

- `AWSLambdaBasicExecutionRole`

Click **Next**

## 5. Role Details

- Role name: `lambda_execution_role`

Click **Create role**

---

# Step 2: Create Lambda Function

## 1. Open Lambda Console

- Search for **Lambda** in AWS Console
- Open Lambda service

## 2. Create Function

Select:

- Author from scratch

### Function Configuration:

- Function name: `devops-lambda`
- Runtime: Python 3.x
- Architecture: x86_64

## 3. Execution Role

- Choose: **Use existing role**
- Select: `lambda_execution_role`

Click **Create function**

---

# Step 3: Add Lambda Code

Replace default code with:

```python
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Welcome to KKE AWS Labs!'
    }
```

---

# Step 4: Deploy Function

- Click **Deploy**

---

# Step 5: Test Lambda Function

## Create Test Event

- Click **Test**
- Event name: `test-event`
- Keep default JSON input
- Save

## Run Test

- Click **Test** again

---

# Expected Output

```json
{
  "statusCode": 200,
  "body": "Welcome to KKE AWS Labs!"
}
```

---

# AWS CLI (Optional)

## Create IAM Role

```bash
aws iam create-role \
  --role-name lambda_execution_role \
  --assume-role-policy-document file://trust-policy.json
```

---

## Attach Policy

```bash
aws iam attach-role-policy \
  --role-name lambda_execution_role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

---

## Create Deployment Package

```bash
zip function.zip lambda_function.py
```

---

## Create Lambda Function

```bash
aws lambda create-function \
  --function-name devops-lambda \
  --runtime python3.12 \
  --role <ROLE_ARN> \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip
```

---

# Validation Checklist

- [ ] IAM role `lambda_execution_role` created
- [ ] Lambda function `devops-lambda` created
- [ ] Runtime set to Python
- [ ] Function deployed successfully
- [ ] Function returns statusCode 200
- [ ] Function returns message "Welcome to KKE AWS Labs!"

---

# Outcome

A working AWS Lambda function named:

- `devops-lambda`

Successfully returns:

```text
Welcome to KKE AWS Labs!
```

with HTTP status code:

```text
200
```

