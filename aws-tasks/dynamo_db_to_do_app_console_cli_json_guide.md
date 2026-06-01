# DynamoDB To-Do Application (Console + CLI + JSON Guide)

This document explains how to create and manage a simple To-Do application using **Amazon DynamoDB** with AWS Management Console, AWS CLI, and JSON item format.

---

## 1. Overview

We will create a DynamoDB table to store tasks for a To-Do application. Each task will include:

- **task_id** (Primary Key)
- **description** (Task details)
- **status** (e.g., in-progress, completed)

---

## 2. Prerequisites

Before starting, ensure you have:

- AWS Account
- Access to AWS Console
- AWS CLI installed and configured
- IAM permissions for DynamoDB

Service used: entity["company","Amazon Web Services","cloud provider"]
Database service: entity["product","Amazon DynamoDB","NoSQL key-value and document database"]

---

## 3. Create DynamoDB Table (AWS Console)

### Step-by-Step:

1. Log in to AWS Console
2. Search for **DynamoDB**
3. Click **Create table**
4. Enter table details:
   - Table name: `ToDoTasks`
   - Partition key: `task_id` (String)
5. Leave default settings or adjust capacity mode (On-demand recommended)
6. Click **Create table**

---

## 4. Create Table Using AWS CLI

### Command:

```bash
aws dynamodb create-table \
  --table-name ToDoTasks \
  --attribute-definitions AttributeName=task_id,AttributeType=S \
  --key-schema AttributeName=task_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

### Verify Table:

```bash
aws dynamodb list-tables
```

---

## 5. Insert Items into Table (CLI)

### Example 1: In-progress task

```bash
aws dynamodb put-item \
  --table-name ToDoTasks \
  --item '{
    "task_id": {"S": "1"},
    "description": {"S": "Setup DynamoDB table"},
    "status": {"S": "in-progress"}
  }'
```

### Example 2: Completed task

```bash
aws dynamodb put-item \
  --table-name ToDoTasks \
  --item '{
    "task_id": {"S": "2"},
    "description": {"S": "Configure AWS CLI"},
    "status": {"S": "completed"}
  }'
```

---

## 6. Insert Item Using JSON File

### Step 1: Create file `item.json`

```json
{
  "task_id": {"S": "3"},
  "description": {"S": "Test DynamoDB integration"},
  "status": {"S": "in-progress"}
}
```

### Step 2: Insert using CLI

```bash
aws dynamodb put-item \
  --table-name ToDoTasks \
  --item file://item.json
```

---

## 7. Retrieve Items

### Scan entire table

```bash
aws dynamodb scan --table-name ToDoTasks
```

### Get specific item

```bash
aws dynamodb get-item \
  --table-name ToDoTasks \
  --key '{"task_id": {"S": "1"}}'
```

---

## 8. Update Item

```bash
aws dynamodb update-item \
  --table-name ToDoTasks \
  --key '{"task_id": {"S": "1"}}' \
  --update-expression "SET #s = :val" \
  --expression-attribute-names '{"#s": "status"}' \
  --expression-attribute-values '{":val": {"S": "completed"}}'
```

---

## 9. Delete Item

```bash
aws dynamodb delete-item \
  --table-name ToDoTasks \
  --key '{"task_id": {"S": "2"}}'
```

---

## 10. JSON Data Model Summary

### Task Item Structure

```json
{
  "task_id": "string (Primary Key)",
  "description": "string",
  "status": "in-progress | completed"
}
```

### Example Dataset

```json
[
  {
    "task_id": "1",
    "description": "Setup DynamoDB table",
    "status": "completed"
  },
  {
    "task_id": "2",
    "description": "Configure AWS CLI",
    "status": "in-progress"
  }
]
```

---

## 11. Conclusion

You now have a fully functional To-Do application backend using DynamoDB with:

- Console setup
- CLI operations
- JSON-based item insertion
- CRUD operations

This setup is ideal for serverless applications and microservices architectures.

