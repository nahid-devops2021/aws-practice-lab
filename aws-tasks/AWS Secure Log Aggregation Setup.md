# AWS Secure Log Aggregation Setup

## Objective

Configure a secure log aggregation pipeline:

```text
xfusion-priv-ec2 (Private VPC)
        |
        | SCP/RSYNC
        v
xfusion-pub-ec2 (Public VPC)
        |
        | AWS CLI
        v
S3 Bucket (xfusion-s3-logs-21534)
```

The file `/var/log/boots.log` from the private EC2 instance must be uploaded to:

```text
s3://xfusion-s3-logs-21534/xfusion-priv-vpc/boot/boots.log
```

---

## Existing Resources

* VPC: `xfusion-priv-vpc`
* Subnet: `xfusion-priv-subnet`
* Route Table: `xfusion-priv-rt`
* EC2 Instance: `xfusion-priv-ec2`
* Key Pair: `xfusion-key.pem`

---

## Step 1: Create Public VPC

1. Navigate to **VPC Console**.
2. Click **Create VPC**.
3. Configure:

   * Name: `xfusion-pub-vpc`
   * IPv4 CIDR: `10.20.0.0/16`
4. Click **Create VPC**.

---

## Step 2: Create Public Subnet

1. Open **VPC → Subnets**.
2. Click **Create Subnet**.
3. Select VPC: `xfusion-pub-vpc`.
4. Configure:

   * Name: `xfusion-pub-subnet`
   * CIDR Block: `10.20.1.0/24`
5. Click **Create Subnet**.

---

## Step 3: Create Public Route Table

1. Open **VPC → Route Tables**.
2. Click **Create Route Table**.
3. Configure:

   * Name: `xfusion-pub-rt`
   * VPC: `xfusion-pub-vpc`
4. Click **Create**.

### Associate Subnet

1. Open `xfusion-pub-rt`.
2. Select **Subnet Associations**.
3. Click **Edit Subnet Associations**.
4. Select `xfusion-pub-subnet`.
5. Save.

---

## Step 4: Create Internet Gateway

1. Open **VPC → Internet Gateways**.
2. Click **Create Internet Gateway**.
3. Name: `xfusion-igw`.
4. Create the gateway.
5. Select the gateway.
6. Click **Actions → Attach to VPC**.
7. Attach to `xfusion-pub-vpc`.

### Configure Internet Route

1. Open route table `xfusion-pub-rt`.
2. Select **Routes → Edit Routes**.
3. Add:

| Destination | Target           |
| ----------- | ---------------- |
| 0.0.0.0/0   | Internet Gateway |

4. Save routes.

---

## Step 5: Launch Public EC2

1. Open **EC2 Console**.
2. Click **Launch Instance**.
3. Configure:

| Setting               | Value              |
| --------------------- | ------------------ |
| Name                  | xfusion-pub-ec2    |
| AMI                   | Ubuntu             |
| Instance Type         | t2.micro           |
| Key Pair              | xfusion-key        |
| VPC                   | xfusion-pub-vpc    |
| Subnet                | xfusion-pub-subnet |
| Auto Assign Public IP | Enabled            |

4. Launch the instance.

---

## Step 6: Create S3 Bucket

1. Open **Amazon S3**.
2. Click **Create Bucket**.
3. Configure:

| Setting       | Value                   |
| ------------- | ----------------------- |
| Bucket Name   | xfusion-s3-logs-21534   |
| Public Access | Block All Public Access |

4. Click **Create Bucket**.

---

## Step 7: Create IAM Role

### Create Policy

Navigate to:

```text
IAM → Policies → Create Policy
```

JSON:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::xfusion-s3-logs-21534/*"
    }
  ]
}
```

Policy Name:

```text
xfusion-s3-put-policy
```

### Create Role

1. Open **IAM → Roles**.
2. Click **Create Role**.
3. Select:

   * Trusted Entity: AWS Service
   * Use Case: EC2
4. Attach policy:

   * `xfusion-s3-put-policy`
5. Role Name:

   * `xfusion-s3-role`
6. Create role.

### Attach Role to EC2

1. Open EC2 Console.
2. Select `xfusion-pub-ec2`.
3. Actions → Security → Modify IAM Role.
4. Select `xfusion-s3-role`.
5. Save.

---

## Step 8: Create VPC Peering

1. Open **VPC → Peering Connections**.
2. Click **Create Peering Connection**.

| Setting       | Value               |
| ------------- | ------------------- |
| Name          | xfusion-vpc-peering |
| Requester VPC | xfusion-pub-vpc     |
| Accepter VPC  | xfusion-priv-vpc    |

3. Click **Create**.

### Accept Request

1. Select peering connection.
2. Actions → Accept Request.

---

## Step 9: Update Route Tables

### Public Route Table

Add route:

| Destination      | Target                 |
| ---------------- | ---------------------- |
| Private VPC CIDR | VPC Peering Connection |

### Private Route Table

Add route:

| Destination  | Target                 |
| ------------ | ---------------------- |
| 10.20.0.0/16 | VPC Peering Connection |

Save both route tables.

---

## Step 10: Configure Security Groups

Allow SSH from private VPC CIDR to the public EC2 instance.

| Type | Port | Source           |
| ---- | ---- | ---------------- |
| SSH  | 22   | Private VPC CIDR |

---

## Step 11: Configure Log Transfer on Private EC2

Edit crontab:

```bash
crontab -e
```

Add:

```cron
*/5 * * * * scp -o StrictHostKeyChecking=no -i /root/.ssh/xfusion-key.pem /var/log/boots.log ubuntu@<PUBLIC-EC2-IP>:/tmp/boots.log
```

Save and exit.

---

## Step 12: Configure Upload to S3 on Public EC2

Install AWS CLI:

```bash
sudo apt update
sudo apt install awscli -y
```

Verify IAM Role:

```bash
aws sts get-caller-identity
```

Edit crontab:

```bash
crontab -e
```

Add:

```cron
*/5 * * * * aws s3 cp /tmp/boots.log s3://xfusion-s3-logs-21534/xfusion-priv-vpc/boot/boots.log
```

Save and exit.

---

## Validation

### Verify file on Public EC2

```bash
ls -l /tmp/boots.log
```

### Verify file in S3

```bash
aws s3 ls s3://xfusion-s3-logs-21534/xfusion-priv-vpc/boot/
```

Expected result:

```text
boots.log
```

---

## Final Outcome

The file:

```text
/var/log/boots.log
```

is automatically copied from:

```text
xfusion-priv-ec2
```

to:

```text
xfusion-pub-ec2
```

and then uploaded to:

```text
s3://xfusion-s3-logs-21534/xfusion-priv-vpc/boot/boots.log
```

using a secure IAM role and a private S3 bucket.
