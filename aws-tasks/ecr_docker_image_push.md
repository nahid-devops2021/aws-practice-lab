# AWS ECR Docker Image Push Guide

## Task Overview

This guide explains how to:

- Create a private ECR repository named `xfusion-ecr`
- Build a Docker image from `/root/pyapp`
- Push the Docker image to Amazon ECR with the `latest` tag

---

# Prerequisites

Ensure the following are installed and configured on the `aws-client` host:

- AWS CLI
- Docker
- Valid AWS credentials
- IAM permissions for ECR access

---

# Step 1: Create ECR Repository

1. Login to AWS Console
2. Navigate to:
   ```
   Elastic Container Registry (ECR)
   ```
3. Click:
   ```
   Create repository
   ```
4. Configure:

| Field | Value |
|---|---|
| Repository type | Private |
| Repository name | xfusion-ecr |

5. Click:
   ```
   Create repository
   ```

---

# Step 2: Open Repository Push Commands

1. Open the newly created repository:
   ```
   xfusion-ecr
   ```
2. Click:
   ```
   View push commands
   ```

AWS will provide authentication and push commands.

---

# Step 3: Login to ECR from aws-client Host

Run the login command provided by AWS Console.

Example:

```bash
aws ecr get-login-password --region us-east-1 | \
docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
```

Replace:

- `<ACCOUNT_ID>` with your AWS account ID
- `us-east-1` with your AWS region

---

# Step 4: Navigate to Application Directory

```bash
cd /root/pyapp
```

---

# Step 5: Build Docker Image

```bash
docker build -t xfusion-ecr .
```

---

# Step 6: Tag Docker Image

```bash
docker tag xfusion-ecr:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/xfusion-ecr:latest
```

---

# Step 7: Push Docker Image to ECR

```bash
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/xfusion-ecr:latest
```

---

# Step 8: Verify Image in AWS Console

1. Go to:
   ```
   ECR → Repositories → xfusion-ecr
   ```
2. Open the repository
3. Verify the image exists with:
   ```
   Tag: latest
   ```

---

# Expected Result

- Private ECR repository created successfully
- Docker image built from `/root/pyapp`
- Docker image pushed successfully to ECR
- Image tag:
  ```
  latest
  ```

