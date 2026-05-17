# AWS NAT Instance Setup for Private EC2 Internet Access

## Objective

Enable internet access for an EC2 instance running in a private subnet using a NAT Instance instead of a NAT Gateway. After successful configuration, the private EC2 instance should be able to upload a test file to the S3 bucket.

---

# Existing Infrastructure

The following resources already exist:

- VPC: `nautilus-priv-vpc`
- Private Subnet: `nautilus-priv-subnet`
- Private EC2 Instance: `nautilus-priv-ec2`
- S3 Bucket: `nautilus-nat-28961`

The private EC2 instance already has a cron job configured to upload `nautilus-test.txt` every minute.

---

# Architecture

```text
Private EC2 Instance
        |
        |
Private Route Table
        |
        |
NAT Instance (Public Subnet)
        |
        |
Internet Gateway
        |
        |
Internet / Amazon S3
```

---

# Step 1: Create Internet Gateway

## AWS Console

Navigate to:

```text
VPC Console → Internet Gateways
```

### Create Internet Gateway

| Setting | Value |
|---|---|
| Name | nautilus-igw |

### Attach Internet Gateway

Attach the gateway to:

```text
nautilus-priv-vpc
```

---

# Step 2: Create Public Subnet

## AWS Console

Navigate to:

```text
VPC Console → Subnets → Create subnet
```

### Configuration

| Setting | Value |
|---|---|
| VPC | nautilus-priv-vpc |
| Subnet Name | nautilus-pub-subnet |
| Availability Zone | Same AZ as private subnet |
| CIDR Block | 10.0.2.0/24 |

Enable:

```text
Auto-assign public IPv4 address
```

---

# Step 3: Create Public Route Table

## AWS Console

Navigate to:

```text
VPC Console → Route Tables
```

### Create Route Table

| Setting | Value |
|---|---|
| Name | nautilus-pub-rt |
| VPC | nautilus-priv-vpc |

---

## Add Route

Edit routes:

| Destination | Target |
|---|---|
| 0.0.0.0/0 | nautilus-igw |

---

## Associate Public Subnet

Associate:

```text
nautilus-pub-subnet
```

---

# Step 4: Create Security Group for NAT Instance

## AWS Console

Navigate to:

```text
EC2 Console → Security Groups
```

### Create Security Group

| Setting | Value |
|---|---|
| Name | nautilus-nat-sg |
| Description | Security group for NAT instance |
| VPC | nautilus-priv-vpc |

---

## Inbound Rules

| Type | Protocol | Port | Source |
|---|---|---|---|
| SSH | TCP | 22 | Your IP |
| All Traffic | All | All | Private subnet CIDR |

---

## Outbound Rules

Allow all outbound traffic.

---

# Step 5: Launch NAT Instance

## AWS Console

Navigate to:

```text
EC2 Console → Launch Instance
```

### Configuration

| Setting | Value |
|---|---|
| Name | nautilus-nat-instance |
| AMI | Amazon Linux 2023 |
| Instance Type | t2.micro |
| Network | nautilus-priv-vpc |
| Subnet | nautilus-pub-subnet |
| Auto Public IP | Enable |
| Security Group | nautilus-nat-sg |

Launch the instance.

---

# Step 6: Disable Source/Destination Check

## AWS Console

Navigate to:

```text
EC2 → Instances → nautilus-nat-instance
```

### Disable Source/Destination Check

Actions:

```text
Networking → Change source/destination check
```

Select:

```text
Disable
```

This step is mandatory for NAT functionality.

---

# Step 7: Configure NAT Instance

## Connect to NAT Instance

```bash
ssh -i <key.pem> ec2-user@<public-ip>
```

---

## Install iptables

Amazon Linux 2023 does not include iptables by default.

Install:

```bash
sudo dnf install iptables-services -y
```

---

## Enable IP Forwarding

Edit sysctl configuration:

```bash
sudo vi /etc/sysctl.conf
```

Add:

```bash
net.ipv4.ip_forward = 1
```

Apply changes:

```bash
sudo sysctl -p
```

Verify:

```bash
sysctl net.ipv4.ip_forward
```

Expected output:

```bash
net.ipv4.ip_forward = 1
```

---

# Step 8: Configure NAT Rules

## Check Network Interface

```bash
ip addr
```

Typically the interface is:

```text
eth0
```

---

## Add MASQUERADE Rule

```bash
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

---

## Allow Forwarding

```bash
sudo iptables -A FORWARD -i eth0 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
```

```bash
sudo iptables -A FORWARD -i eth0 -o eth0 -j ACCEPT
```

---

## Save iptables Rules

```bash
sudo service iptables save
```

---

## Enable and Start iptables Service

```bash
sudo systemctl enable iptables
sudo systemctl start iptables
```

---

# Step 9: Update Private Route Table

## AWS Console

Navigate to:

```text
VPC Console → Route Tables
```

Locate the route table associated with:

```text
nautilus-priv-subnet
```

---

## Add Default Route

Edit routes:

| Destination | Target |
|---|---|
| 0.0.0.0/0 | nautilus-nat-instance |

Save changes.

This route allows outbound internet traffic from the private subnet through the NAT instance.

---

# Step 10: Verify Internet Connectivity

SSH into the private EC2 instance if required.

Test internet connectivity:

```bash
ping google.com
```

Or:

```bash
curl https://aws.amazon.com
```

---

# Step 11: Verify S3 Upload

After 1–2 minutes, verify the file upload in the S3 bucket.

## Bucket

```text
nautilus-nat-28961
```

## Expected File

```text
nautilus-test.txt
```

If the file exists in the bucket, internet access through the NAT instance is working successfully.

---

# Useful iptables Commands

## List All Rules

```bash
sudo iptables -L -n -v
```

---

## List NAT Table Rules

```bash
sudo iptables -t nat -L -n -v
```

---

## List Rules with Line Numbers

```bash
sudo iptables -L --line-numbers -n -v
```

```bash
sudo iptables -t nat -L --line-numbers -n -v
```

---

## Remove a Rule by Number

Example:

```bash
sudo iptables -t nat -D POSTROUTING 1
```

Format:

```bash
sudo iptables -t nat -D <CHAIN_NAME> <RULE_NUMBER>
```

---

## Save Updated Rules

```bash
sudo service iptables save
```

---

# Troubleshooting

## Common Issues

### 1. Source/Destination Check Not Disabled

NAT will not function unless source/destination check is disabled.

---

### 2. Missing Default Route in Private Route Table

Ensure:

| Destination | Target |
|---|---|
| 0.0.0.0/0 | NAT Instance |

---

### 3. iptables Service Not Running

Check:

```bash
sudo systemctl status iptables
```

---

### 4. IP Forwarding Disabled

Verify:

```bash
sysctl net.ipv4.ip_forward
```

Expected:

```bash
net.ipv4.ip_forward = 1
```

---

# Final Validation Checklist

| Task | Status |
|---|---|
| Internet Gateway Created | Completed |
| Public Subnet Created | Completed |
| Public Route Table Configured | Completed |
| NAT Security Group Created | Completed |
| NAT Instance Launched | Completed |
| Source/Destination Check Disabled | Completed |
| IP Forwarding Enabled | Completed |
| iptables NAT Rules Configured | Completed |
| Private Route Table Updated | Completed |
| S3 Upload Verified | Completed |

---

# Result

The private EC2 instance successfully accesses the internet through the NAT Instance and uploads the test file to Amazon S3.

