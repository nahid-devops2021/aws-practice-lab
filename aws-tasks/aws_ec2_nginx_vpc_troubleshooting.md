# AWS EC2 Nginx Internet Accessibility Troubleshooting Guide

## Overview

The Nautilus Development Team deployed a web application on an AWS EC2 instance running Nginx inside a public VPC named `datacenter-vpc`. Although the security group allowed HTTP traffic on port `80`, the application was still inaccessible from the internet.

This document explains how to troubleshoot and resolve the issue by verifying:

- VPC internet connectivity
- Internet Gateway configuration
- Route table settings
- Security group rules
- Network ACL rules
- EC2 public accessibility
- Nginx service availability

---

# Architecture Diagram

```text
                Internet
                    │
                    ▼
         ┌────────────────────┐
         │ Internet Gateway   │
         └────────────────────┘
                    │
                    ▼
         ┌────────────────────┐
         │ Route Table        │
         │ 0.0.0.0/0 → IGW    │
         └────────────────────┘
                    │
                    ▼
         ┌────────────────────┐
         │ Public Subnet      │
         └────────────────────┘
                    │
                    ▼
         ┌────────────────────┐
         │ EC2 Instance       │
         │ datacenter-ec2     │
         │ Nginx Port 80      │
         └────────────────────┘
```

---

# Task Objective

Ensure that:

- The VPC `datacenter-vpc` is configured for internet access.
- The EC2 instance `datacenter-ec2` is publicly accessible.
- The Nginx application is reachable from the internet on port `80`.

---

# Step 1: Verify EC2 Instance Public Accessibility

## Navigate to EC2 Console

```text
AWS Console → EC2 → Instances
```

Select:

```text
datacenter-ec2
```

Verify:

- Instance State = `Running`
- Public IPv4 address exists

Example:

```text
54.xx.xx.xx
```

---

## If Public IP is Missing

### Allocate and Attach Elastic IP

Navigate to:

```text
EC2 → Elastic IPs
```

Steps:

1. Click `Allocate Elastic IP`
2. Select the allocated IP
3. Click `Actions → Associate Elastic IP`
4. Select:
   - Instance: `datacenter-ec2`

---

# Step 2: Verify Security Group Configuration

Navigate to:

```text
EC2 → Security Groups → datacenter-sg
```

## Required Inbound Rules

| Type | Protocol | Port | Source |
|------|-----------|------|---------|
| HTTP | TCP | 80 | 0.0.0.0/0 |

Optional IPv6 Rule:

| Type | Protocol | Port | Source |
|------|-----------|------|---------|
| HTTP | TCP | 80 | ::/0 |

---

# Step 3: Verify Network ACL Configuration

Navigate to:

```text
VPC → Network ACLs
```

Find the NACL associated with the EC2 subnet.

---

## Required Inbound Rules

| Rule | Type | Protocol | Port Range | Source | Allow/Deny |
|------|------|-----------|-------------|---------|-------------|
| 100 | HTTP | TCP | 80 | 0.0.0.0/0 | ALLOW |
| 110 | Ephemeral | TCP | 1024-65535 | 0.0.0.0/0 | ALLOW |

---

## Required Outbound Rules

| Rule | Type | Protocol | Port Range | Destination | Allow/Deny |
|------|------|-----------|-------------|-------------|-------------|
| 100 | HTTP | TCP | 80 | 0.0.0.0/0 | ALLOW |
| 110 | Ephemeral | TCP | 1024-65535 | 0.0.0.0/0 | ALLOW |

---

# Step 4: Verify Internet Gateway Configuration

Navigate to:

```text
VPC → Internet Gateways
```

Verify that an Internet Gateway is attached to:

```text
datacenter-vpc
```

---

## If Internet Gateway is Missing

### Create Internet Gateway

```text
VPC → Internet Gateways → Create internet gateway
```

Name:

```text
datacenter-igw
```

---

### Attach Internet Gateway to VPC

```text
Actions → Attach to VPC
```

Select:

```text
datacenter-vpc
```

---

# Step 5: Verify Route Table Configuration

Navigate to:

```text
VPC → Route Tables
```

Locate the route table associated with the public subnet.

---

## Required Route

| Destination | Target |
|-------------|--------|
| 0.0.0.0/0 | Internet Gateway |

Example:

```text
0.0.0.0/0 → igw-xxxxxxxx
```

---

## Add Route If Missing

Click:

```text
Edit Routes → Add Route
```

Configure:

| Destination | Target |
|-------------|--------|
| 0.0.0.0/0 | Internet Gateway |

Save changes.

---

# Step 6: Verify Subnet Association

Open the route table and verify subnet associations.

Navigate:

```text
Route Table → Subnet Associations
```

Ensure the subnet containing `datacenter-ec2` is associated with the public route table.

---

# Step 7: Verify Nginx Service

SSH into the EC2 instance:

```bash
ssh -i key.pem ec2-user@PUBLIC_IP
```

Check Nginx service status:

```bash
sudo systemctl status nginx
```

---

## Start Nginx If Stopped

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

---

# Step 8: Verify Port 80 is Listening

Run:

```bash
sudo ss -tulpn | grep :80
```

Expected Output:

```text
LISTEN 0 511 0.0.0.0:80
```

---

# Step 9: Test Application Locally

Run:

```bash
curl localhost
```

Expected Output:

```html
Welcome to nginx!
```

---

# Step 10: Verify External Accessibility

Open a browser:

```text
http://PUBLIC_IP
```

Or test using curl:

```bash
curl http://PUBLIC_IP
```

Expected Output:

```html
Welcome to nginx!
```

---

# AWS CLI Verification Commands

## Verify Public IP

```bash
aws ec2 describe-instances \
--filters "Name=tag:Name,Values=datacenter-ec2" \
--query "Reservations[*].Instances[*].PublicIpAddress"
```

---

## Verify Internet Gateway

```bash
aws ec2 describe-internet-gateways
```

---

## Verify Route Tables

```bash
aws ec2 describe-route-tables
```

---

## Verify Security Group Rules

```bash
aws ec2 describe-security-groups \
--group-names datacenter-sg
```

---

# Common Root Causes

| Problem | Solution |
|---------|-----------|
| No Internet Gateway attached | Attach IGW to VPC |
| Missing default route | Add `0.0.0.0/0 → IGW` |
| No Public IP | Assign Elastic IP |
| Security Group blocking HTTP | Allow TCP port 80 |
| NACL blocking traffic | Allow inbound/outbound rules |
| Nginx stopped | Start Nginx service |
| Wrong subnet association | Associate correct route table |

---

# Final Expected Configuration

| Component | Expected State |
|-----------|----------------|
| EC2 Instance | Running |
| Public IP | Assigned |
| Security Group | HTTP port 80 allowed |
| Internet Gateway | Attached |
| Route Table | `0.0.0.0/0 → IGW` |
| Public Subnet | Associated |
| Nginx Service | Running |
| Port 80 | Listening |

---

# Result

After completing the troubleshooting steps:

- The VPC `datacenter-vpc` will support internet connectivity.
- The EC2 instance `datacenter-ec2` will be publicly accessible.
- The Nginx application will successfully respond on port `80`.

---

# Conclusion

This troubleshooting process ensures proper AWS VPC internet routing and confirms that all networking layers required for public access are correctly configured.

The most common root cause in these scenarios is usually:

- Missing Internet Gateway
- Missing `0.0.0.0/0` route
- No public IP attached to the EC2 instance

Once these are corrected, the application becomes accessible from the internet.

