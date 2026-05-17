# AWS Private RDS MySQL Instance Setup Guide

## Objective

Provision a private Amazon RDS MySQL instance using the AWS Free Tier for development and testing purposes.

The RDS instance must:

- Be named `datacenter-rds`
- Use MySQL engine version `8.4.x`
- Use the `Free tier` template
- Use instance class `db.t3.micro`
- Enable storage autoscaling with maximum threshold set to `50 GB`
- Remain private (not publicly accessible)
- Reach the `Available` state successfully

---

# Requirements

| Component | Value |
|---|---|
| DB Identifier | datacenter-rds |
| Engine | MySQL |
| Engine Version | 8.4.x |
| Template | Free tier |
| Instance Type | db.t3.micro |
| Accessibility | Private |
| Storage Autoscaling | Enabled |
| Maximum Storage Threshold | 50 GB |

---

# Step 1: Open RDS Console

Navigate to:

```text
AWS Console → RDS
```

---

# Step 2: Create Database

Click:

```text
Create database
```

---

# Step 3: Select Database Creation Method

Choose:

```text
Standard create
```

Database creation method:

```text
Full configuration
```

---

# Step 4: Select Engine Options

## Engine Type

Choose:

```text
MySQL
```

## Engine Version

Select:

```text
MySQL 8.4.x
```

Example:

```text
8.4.3
```

---

# Step 5: Choose Template

Under Templates select:

```text
Free tier
```

---

# Step 6: Configure DB Settings

## DB Instance Identifier

Set:

```text
datacenter-rds
```

---

## Master Username

Example:

```text
admin
```

---

## Credentials

Choose one of the following:

### Option 1: Self-managed Password

Set:

```text
Master password
Confirm password
```

### Option 2: Auto Generate Password

Enable:

```text
Auto generate a password
```

---

# Step 7: Configure Instance Class

Under DB instance class select:

```text
Burstable classes (includes t classes)
```

Select:

```text
db.t3.micro
```

---

# Step 8: Configure Storage

## Allocated Storage

Keep default Free Tier storage.

Example:

```text
20 GiB
```

---

## Enable Storage Autoscaling

Enable:

```text
Enable storage autoscaling
```

Set maximum storage threshold:

```text
50 GB
```

Keep remaining storage settings as default.

---

# Step 9: Configure Connectivity

## Virtual Private Cloud (VPC)

Select the required VPC.

Example:

```text
Default VPC
```

or

```text
Existing project VPC
```

---

## Public Access

Set:

```text
No
```

This ensures the RDS instance remains private.

---

## VPC Security Group

Choose:

```text
Create new
```

or use an existing private security group.

Example:

```text
datacenter-rds-sg
```

---

## Availability Zone

Keep default.

---

# Step 10: Additional Configuration

Keep all remaining settings as default.

This includes:

- Automated backups
- Monitoring
- Maintenance
- Deletion protection
- Log exports
- Encryption

---

# Step 11: Create Database

Click:

```text
Create database
```

---

# Step 12: Verify RDS Status

Navigate to:

```text
RDS Console → Databases
```

Locate:

```text
datacenter-rds
```

Verify status:

```text
Available
```

---

# Validation Checklist

| Validation Item | Expected Result |
|---|---|
| RDS Instance Name | datacenter-rds |
| Database Engine | MySQL |
| Engine Version | 8.4.x |
| Template | Free tier |
| Instance Class | db.t3.micro |
| Public Access | Disabled |
| Storage Autoscaling | Enabled |
| Max Storage Threshold | 50 GB |
| Instance State | Available |

---

# Security Recommendations

## Restrict Database Access

Allow MySQL access only from trusted EC2 instances or application security groups.

Recommended inbound rule:

| Type | Port | Source |
|---|---|---|
| MySQL/Aurora | 3306 | Application Security Group |

Avoid allowing:

```text
0.0.0.0/0
```

for database access.

---

# Troubleshooting

## Common Issues

### 1. DB Instance Stuck in Creating State

Wait several minutes as RDS provisioning may take time.

---

### 2. db.t3.micro Option Not Visible

Ensure:

- Free tier template is selected
- Correct region is used

---

### 3. Public Access Enabled Accidentally

Modify database:

```text
Connectivity → Public access → No
```

Apply immediately.

---

### 4. Unable to Connect from EC2

Verify:

- Security group inbound rules
- Same VPC configuration
- Port 3306 access allowed

---

# Optional Connectivity Test

From an EC2 instance inside the same VPC:

Install MySQL client:

```bash
sudo dnf install mysql -y
```

Connect:

```bash
mysql -h <rds-endpoint> -u admin -p
```

---

# Result

The private Amazon RDS MySQL instance `datacenter-rds` has been successfully provisioned using the AWS Free Tier configuration with storage autoscaling enabled.

