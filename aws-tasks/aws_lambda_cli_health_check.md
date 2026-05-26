# AWS Lambda CLI Health Check Runbook

## Objective

This document explains how to verify and monitor an AWS Lambda function using AWS CLI to ensure it is working correctly.

The target function used in this runbook:

- Function Name: `nautilus-lambda-cli`

---

## Prerequisites

- AWS CLI installed and configured
- IAM permissions for AWS Lambda and CloudWatch Logs
- Existing Lambda function deployed

---

# 1. Check If Lambda Function Exists

Verify the function is created successfully:

```bash
aws lambda list-functions
```

To check a specific function:

```bash
aws lambda get-function \
  --function-name nautilus-lambda-cli
```

### Expected Output
- Function metadata (ARN, runtime, handler, role)

---

# 2. Check Lambda Configuration

Validate runtime, handler, and status:

```bash
aws lambda get-function-configuration \
  --function-name nautilus-lambda-cli
```

### Key Fields to Verify

| Field | Expected Value |
|------|------|
| Runtime | python3.x |
| Handler | lambda_function.lambda_handler |
| State | Active |

---

# 3. Invoke Lambda Function (Functional Test)

Run a test invocation:

```bash
aws lambda invoke \
  --function-name nautilus-lambda-cli \
  response.json
```

---

## 4. View Response Output

Check the output file:

```bash
cat response.json
```

### Expected Output

```json
{
  "statusCode": 200,
  "body": "Welcome to KKE AWS Labs!"
}
```

---

# 5. Check CloudWatch Logs

Lambda automatically sends logs to CloudWatch.

### List Log Groups

```bash
aws logs describe-log-groups
```

Look for:

```
/aws/lambda/nautilus-lambda-cli
```

---

### Stream Logs in Real-Time

```bash
aws logs tail /aws/lambda/nautilus-lambda-cli --follow
```

---

# 6. Check Latest Execution Status

Verify last update status:

```bash
aws lambda get-function-configuration \
  --function-name nautilus-lambda-cli \
  --query "LastUpdateStatus"
```

### Expected Value

```
Successful
```

---

# 7. One-Line Health Check

Quick validation command:

```bash
aws lambda invoke --function-name nautilus-lambda-cli /tmp/output.json && cat /tmp/output.json
```

---

# Validation Checklist

- [ ] Lambda function exists
- [ ] Configuration is correct
- [ ] Function runtime is valid
- [ ] Invocation returns status code 200
- [ ] Response body is correct
- [ ] CloudWatch logs are generated

---

# Expected Result

The Lambda function should return:

```text
Welcome to KKE AWS Labs!
```

with status code:

```text
200
```

---

# Notes

- Ensure IAM role has `AWSLambdaBasicExecutionRole`
- Ensure correct handler format: `lambda_function.lambda_handler`
- Always check CloudWatch logs for debugging failures

