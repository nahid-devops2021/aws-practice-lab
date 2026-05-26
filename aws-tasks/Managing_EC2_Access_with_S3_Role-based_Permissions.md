# 🚀 Managing EC2 Access with S3 Role-based Permissions (Console + CLI Guide)

## 📌 Overview
This document explains how to set up EC2 access to a private S3 bucket using IAM Role, SSH keys, and AWS Console + CLI.

---

# 🧱 Architecture

```
aws-client (SSH keys)
        │
        ▼
datacenter-ec2 (EC2 Instance)
        │
        ▼
IAM Role (datacenter-role)
        │
        ▼
S3 Bucket (datacenter-s3-958494834452)
```

---

# 1️⃣ EC2 Instance Check (Console)

- Go to AWS Console → EC2 → Instances
- Search: datacenter-ec2
- Ensure:
  - Running ✔
  - Public IP available ✔

---

# 2️⃣ SSH Key Setup (aws-client)

## Generate SSH key
```bash
ssh-keygen -t rsa -b 4096 -f id_rsa
```

## Add key to EC2

SSH into EC2:
```bash
ssh ec2-user@<EC2_PUBLIC_IP>
```

On EC2:
```bash
sudo mkdir -p /root/.ssh
sudo chmod 700 /root/.ssh
```

Copy public key:
```bash
cat id_rsa.pub
```

Paste into:
```bash
sudo nano /root/.ssh/authorized_keys
```

Fix permissions:
```bash
sudo chmod 600 /root/.ssh/authorized_keys
sudo chown -R root:root /root/.ssh
```

---

# 3️⃣ Create S3 Bucket (Console)

- Go to S3 → Create bucket
- Bucket name: datacenter-s3-958494834452
- Block Public Access: ENABLED ✔
- Click Create

Verify:
- Permissions → Block Public Access ON

---

# 4️⃣ IAM Policy + Role (Console)

## Create IAM Policy

IAM → Policies → Create policy → JSON:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::datacenter-s3-958494834452",
        "arn:aws:s3:::datacenter-s3-958494834452/*"
      ]
    }
  ]
}
```

Name: datacenter-s3-policy

---

## Create IAM Role

- IAM → Roles → Create role
- Trusted entity: EC2
- Attach policy: datacenter-s3-policy
- Role name: datacenter-role

---

## Attach Role to EC2

EC2 → Instances → datacenter-ec2

Actions:
- Security → Modify IAM role
- Select: datacenter-role

---

# 5️⃣ Test S3 Access (EC2)

SSH into EC2:
```bash
ssh -i id_rsa root@<EC2_PUBLIC_IP>
```

Create file:
```bash
echo "S3 test file" > testfile.txt
```

Upload:
```bash
aws s3 cp testfile.txt s3://datacenter-s3-958494834452/
```

List:
```bash
aws s3 ls s3://datacenter-s3-958494834452/
```

Expected:
```
testfile.txt
```

---

# 🎯 Outcome

✔ EC2 securely accesses S3  
✔ IAM Role used (no access keys)  
✔ Private S3 bucket  
✔ File upload successful  
