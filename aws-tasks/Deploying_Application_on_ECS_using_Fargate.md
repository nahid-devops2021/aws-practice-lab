# Deploying a Containerized Application with Amazon ECR and ECS (Fargate)

## Overview

This guide explains how to:

- Create a private Amazon ECR repository
- Build and push a Docker image
- Create an ECS cluster using Fargate
- Create a task definition
- Deploy the application using an ECS service

---

# Architecture Overview

```text
+-------------------+
|   aws-client VM   |
|-------------------|
| Docker Build      |
| AWS CLI           |
+---------+---------+
          |
          | Push Image
          v
+-------------------+
| Amazon ECR        |
| xfusion-ecr       |
+---------+---------+
          |
          | Pull Image
          v
+-------------------+
| Amazon ECS        |
| xfusion-cluster   |
| Fargate Tasks     |
+---------+---------+
          |
          v
+-------------------+
| xfusion-service   |
| Running Container |
+-------------------+
```

---

# Prerequisites

Ensure the following are installed/configured on the `aws-client` host:

- AWS CLI configured
- Docker installed and running
- IAM permissions for:
  - ECR
  - ECS
  - IAM PassRole
  - CloudWatch Logs

---

# Step 1: Create a Private ECR Repository

Run the following command:

```bash
aws ecr create-repository \
  --repository-name xfusion-ecr
```

Expected output:

```json
{
  "repository": {
    "repositoryName": "xfusion-ecr",
    "repositoryUri": "ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/xfusion-ecr"
  }
}
```

Save the `repositoryUri`.

Example:

```bash
123456789012.dkr.ecr.us-east-1.amazonaws.com/xfusion-ecr
```

---

# Step 2: Authenticate Docker to Amazon ECR

Authenticate Docker with ECR:

```bash
aws ecr get-login-password --region us-east-1 | \
docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
```

Replace:

- `ACCOUNT_ID`
- `REGION`

---

# Step 3: Build Docker Image

Move to the application directory:

```bash
cd /root/pyapp
```

Build the Docker image:

```bash
docker build -t xfusion-ecr:latest .
```

Verify image:

```bash
docker images
```

---

# Step 4: Tag Docker Image

Tag the image for ECR:

```bash
docker tag xfusion-ecr:latest \
ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/xfusion-ecr:latest
```

Example:

```bash
docker tag xfusion-ecr:latest \
123456789012.dkr.ecr.us-east-1.amazonaws.com/xfusion-ecr:latest
```

---

# Step 5: Push Image to ECR

Push the image:

```bash
docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/xfusion-ecr:latest
```

Verify the image exists:

```bash
aws ecr list-images \
  --repository-name xfusion-ecr
```

---

# Step 6: Create ECS Cluster (Fargate)

Create the ECS cluster:

```bash
aws ecs create-cluster \
  --cluster-name xfusion-cluster
```

Verify cluster:

```bash
aws ecs list-clusters
```

---

# Step 7: Create ECS Task Execution Role

Create a file named `ecs-trust-policy.json`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Create the IAM role:

```bash
aws iam create-role \
  --role-name ecsTaskExecutionRole \
  --assume-role-policy-document file://ecs-trust-policy.json
```

Attach the required policy:

```bash
aws iam attach-role-policy \
  --role-name ecsTaskExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

---

# Step 8: Create ECS Task Definition

Create a file named `task-definition.json`

```json
{
  "family": "xfusion-taskdefinition",
  "networkMode": "awsvpc",
  "requiresCompatibilities": [
    "FARGATE"
  ],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "xfusion-container",
      "image": "ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/xfusion-ecr:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 80,
          "hostPort": 80,
          "protocol": "tcp"
        }
      ]
    }
  ]
}
```

Replace:

- `ACCOUNT_ID`
- `REGION`

Register the task definition:

```bash
aws ecs register-task-definition \
  --cli-input-json file://task-definition.json
```

---

# Step 9: Create Security Group

Create a security group:

```bash
aws ec2 create-security-group \
  --group-name xfusion-ecs-sg \
  --description "ECS Security Group" \
  --vpc-id VPC_ID
```

Allow HTTP traffic:

```bash
aws ec2 authorize-security-group-ingress \
  --group-id SG_ID \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0
```

---

# Step 10: Create ECS Service

Get subnet IDs:

```bash
aws ec2 describe-subnets
```

Create the ECS service:

```bash
aws ecs create-service \
  --cluster xfusion-cluster \
  --service-name xfusion-service \
  --task-definition xfusion-taskdefinition \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxxxx],securityGroups=[sg-xxxxxxx],assignPublicIp=ENABLED}"
```

Example:

```bash
aws ecs create-service \
  --cluster xfusion-cluster \
  --service-name xfusion-service \
  --task-definition xfusion-taskdefinition \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}"
```

---

# Step 11: Verify Running Tasks

Check service status:

```bash
aws ecs describe-services \
  --cluster xfusion-cluster \
  --services xfusion-service
```

List running tasks:

```bash
aws ecs list-tasks \
  --cluster xfusion-cluster
```

Describe task:

```bash
aws ecs describe-tasks \
  --cluster xfusion-cluster \
  --tasks TASK_ID
```

---

# Cleanup Commands

## Scale Service to Zero

```bash
aws ecs update-service \
  --cluster xfusion-cluster \
  --service xfusion-service \
  --desired-count 0
```

## Delete ECS Service

```bash
aws ecs delete-service \
  --cluster xfusion-cluster \
  --service xfusion-service \
  --force
```

## Delete ECS Cluster

```bash
aws ecs delete-cluster \
  --cluster xfusion-cluster
```

## Delete ECR Repository

```bash
aws ecr delete-repository \
  --repository-name xfusion-ecr \
  --force
```

---

# AWS Console Steps

## Create ECR Repository

1. Open Amazon ECR Console
2. Click **Create repository**
3. Select:
   - Private
   - Repository name: `xfusion-ecr`
4. Click **Create repository**

---

## Create ECS Cluster

1. Open Amazon ECS Console
2. Go to **Clusters**
3. Click **Create Cluster**
4. Select:
   - Networking only (Fargate)
5. Cluster name:
   - `xfusion-cluster`
6. Click **Create**

---

## Create Task Definition

1. ECS Console → **Task Definitions**
2. Click **Create new Task Definition**
3. Select:
   - Fargate
4. Configure:
   - Name: `xfusion-taskdefinition`
   - CPU: `0.25 vCPU`
   - Memory: `0.5 GB`
5. Add container:
   - Image URI from ECR
   - Port: `80`
6. Save

---

## Create ECS Service

1. Open cluster `xfusion-cluster`
2. Click **Create**
3. Configure:
   - Launch type: Fargate
   - Task definition: `xfusion-taskdefinition`
   - Service name: `xfusion-service`
   - Desired tasks: `1`
4. Configure networking:
   - Select VPC
   - Select subnets
   - Attach security group
   - Enable public IP
5. Click **Create**

---

# Final Validation

Verify all resources:

```bash
aws ecr describe-repositories

aws ecs list-clusters

aws ecs list-services \
  --cluster xfusion-cluster

aws ecs list-tasks \
  --cluster xfusion-cluster
```

---

# Expected Result

After completing all steps:

- Private ECR repository `xfusion-ecr` exists
- Docker image successfully pushed to ECR
- ECS cluster `xfusion-cluster` created
- ECS task definition registered
- ECS service `xfusion-service` running
- At least one Fargate task is healthy
