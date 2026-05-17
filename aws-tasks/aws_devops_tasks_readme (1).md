# AWS DevOps Tasks Documentation

## 1. Enable Stop Protection for EC2 Instance

### Task
Enable stop protection for EC2 instance `nautilus-ec2` in `us-east-1` region.

### AWS CLI Commands
```bash
# Get instance ID
aws ec2 describe-instances \
  --region us-east-1 \
  --filters "Name=tag:Name,Values=nautilus-ec2" \
  --query "Reservations[].Instances[].InstanceId" \
  --output text

# Enable stop protection
aws ec2 modify-instance-attribute \
  --region us-east-1 \
  --instance-id <INSTANCE_ID> \
  --disable-api-stop '{"Value":true}'

# Verify
aws ec2 describe-instance-attribute \
  --region us-east-1 \
  --instance-id <INSTANCE_ID> \
  --attribute disableApiStop
```

---

# 2. Attach ENI to EC2 Instance

### Task
Attach existing ENI `nautilus-eni` to EC2 instance `nautilus-ec2`.

### AWS CLI Commands
```bash
# Get instance ID
aws ec2 describe-instances \
  --region us-east-1 \
  --filters "Name=tag:Name,Values=nautilus-ec2" \
  --query "Reservations[].Instances[].InstanceId" \
  --output text

# Get ENI ID
aws ec2 describe-network-interfaces \
  --region us-east-1 \
  --filters "Name=tag:Name,Values=nautilus-eni" \
  --query "NetworkInterfaces[].NetworkInterfaceId" \
  --output text

# Attach ENI
aws ec2 attach-network-interface \
  --region us-east-1 \
  --network-interface-id <ENI_ID> \
  --instance-id <INSTANCE_ID> \
  --device-index 1

# Verify
aws ec2 describe-network-interfaces \
  --region us-east-1 \
  --network-interface-ids <ENI_ID> \
  --query "NetworkInterfaces[].Status"
```

---

# 3. Create AMI from Existing EC2 Instance

### Task
Create an AMI named `nautilus-ec2-ami` from EC2 instance `nautilus-ec2`.

### AWS CLI Commands
```bash
# Get instance ID
aws ec2 describe-instances \
  --region us-east-1 \
  --filters "Name=tag:Name,Values=nautilus-ec2" \
  --query "Reservations[].Instances[].InstanceId" \
  --output text

# Create AMI
aws ec2 create-image \
  --region us-east-1 \
  --instance-id <INSTANCE_ID> \
  --name "nautilus-ec2-ami" \
  --no-reboot

# Wait for availability
aws ec2 wait image-available \
  --region us-east-1 \
  --image-ids <AMI_ID>

# Verify
aws ec2 describe-images \
  --region us-east-1 \
  --image-ids <AMI_ID> \
  --query "Images[].State"
```

---

# 4. Delete EC2 Instance

### Task
Delete EC2 instance `datacenter-ec2` and ensure it reaches terminated state.

### AWS CLI Commands
```bash
# Get instance ID
aws ec2 describe-instances \
  --region us-east-1 \
  --filters "Name=tag:Name,Values=datacenter-ec2" \
  --query "Reservations[].Instances[].InstanceId" \
  --output text

# Terminate instance
aws ec2 terminate-instances \
  --region us-east-1 \
  --instance-ids <INSTANCE_ID>

# Wait until terminated
aws ec2 wait instance-terminated \
  --region us-east-1 \
  --instance-ids <INSTANCE_ID>
```

---

# 5. Create IAM Policy

### Task
Create IAM policy `iampolicy_jim` with EC2 read-only access.

### Policy JSON
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeImages",
        "ec2:DescribeSnapshots",
        "ec2:DescribeVolumes",
        "ec2:DescribeSecurityGroups",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DescribeTags",
        "ec2:DescribeRegions",
        "ec2:DescribeAvailabilityZones"
      ],
      "Resource": "*"
    }
  ]
}
```

### Create Policy
```bash
aws iam create-policy \
  --policy-name iampolicy_jim \
  --policy-document file://ec2-readonly.json
```

---

# 6. Create EC2 Instance with Passwordless SSH

### Task
Create EC2 instance `devops-ec2` and configure passwordless SSH from `aws-client`.

### Generate SSH Key
```bash
mkdir -p /root/.ssh
[ -f /root/.ssh/id_rsa ] || ssh-keygen -t rsa -b 2048 -f /root/.ssh/id_rsa -N ""
```

### Get Public Key
```bash
cat /root/.ssh/id_rsa.pub
```

### Launch EC2 Instance
```bash
aws ec2 run-instances \
  --region us-east-1 \
  --image-id <AMI_ID> \
  --instance-type t2.micro \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=devops-ec2}]'
```

### Add Public Key to EC2
```bash
mkdir -p /root/.ssh
chmod 700 /root/.ssh

echo "<PUBLIC_KEY>" >> /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys
```

### Test SSH
```bash
ssh -i /root/.ssh/id_rsa root@<EC2_PUBLIC_IP>
```

---

# 7. Create Private S3 Bucket and Migrate Data

### Task
Create bucket `xfusion-sync-15888` and migrate data from `xfusion-s3-25260`.

### AWS CLI Commands
```bash
# Create bucket
aws s3api create-bucket \
  --bucket xfusion-sync-15888 \
  --region us-east-1

# Block public access
aws s3api put-public-access-block \
  --bucket xfusion-sync-15888 \
  --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

# Sync data
aws s3 sync s3://xfusion-s3-25260 s3://xfusion-sync-15888

# Verify consistency
aws s3 sync s3://xfusion-s3-25260 s3://xfusion-sync-15888 --dryrun
```

---

# 8. Configure Application Load Balancer

### Task
- Create ALB `xfusion-alb`
- Create target group `xfusion-tg`
- Create security group `xfusion-sg`
- Route traffic from ALB to `xfusion-ec2`

### Create Security Group
```bash
aws ec2 create-security-group \
  --group-name xfusion-sg \
  --description "Allow HTTP" \
  --vpc-id <VPC_ID>

aws ec2 authorize-security-group-ingress \
  --group-id <SG_ID> \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0
```

### Create Target Group
```bash
aws elbv2 create-target-group \
  --name xfusion-tg \
  --protocol HTTP \
  --port 80 \
  --vpc-id <VPC_ID> \
  --target-type instance
```

### Register Target
```bash
aws elbv2 register-targets \
  --target-group-arn <TG_ARN> \
  --targets Id=<INSTANCE_ID>
```

### Create ALB
```bash
aws elbv2 create-load-balancer \
  --name xfusion-alb \
  --subnets <SUBNET_1> <SUBNET_2> \
  --security-groups <SG_ID> \
  --scheme internet-facing \
  --type application
```

### Create Listener
```bash
aws elbv2 create-listener \
  --load-balancer-arn <ALB_ARN> \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=<TG_ARN>
```

### Update EC2 Security Group
```bash
aws ec2 authorize-security-group-ingress \
  --group-id <EC2_SG_ID> \
  --protocol tcp \
  --port 80 \
  --source-group <SG_ID>
```

---

# 9. ALB Troubleshooting

### Issue
Target status showed:
```text
Unused: Target is in an Availability Zone that is not enabled for the load balancer
```

### Root Cause
ALB and EC2 were in different Availability Zones.

### Fix
1. Open EC2 Console.
2. Go to Load Balancers.
3. Select the ALB.
4. Open Network Mapping.
5. Edit subnets.
6. Add subnet from the same AZ as EC2 instance.
7. Save changes.

### Verify
- Target status changes to `healthy`
- ALB DNS serves the application

---

# AWS Console Steps

## Enable Stop Protection for EC2 Instance
1. Open AWS Console.
2. Go to EC2 Dashboard.
3. Select region `us-east-1`.
4. Click Instances.
5. Select `nautilus-ec2`.
6. Click Actions → Instance Settings → Change Stop Protection.
7. Enable Stop Protection.
8. Save changes.

---

## Attach ENI to EC2 Instance
1. Open EC2 Dashboard.
2. Go to Network Interfaces.
3. Select `nautilus-eni`.
4. Click Actions → Attach.
5. Select instance `nautilus-ec2`.
6. Set Device Index = 1.
7. Click Attach.
8. Verify status becomes `attached`.

---

## Create AMI from Existing EC2 Instance
1. Open EC2 Dashboard.
2. Select instance `nautilus-ec2`.
3. Click Actions → Image and Templates → Create Image.
4. Enter AMI name: `nautilus-ec2-ami`.
5. Click Create Image.
6. Go to AMIs section.
7. Wait until status becomes `available`.

---

## Delete EC2 Instance
1. Open EC2 Dashboard.
2. Select instance `datacenter-ec2`.
3. Click Instance State → Terminate Instance.
4. Confirm termination.
5. Wait until instance state becomes `terminated`.

---

## Create IAM Policy
1. Open IAM Dashboard.
2. Click Policies → Create Policy.
3. Open JSON tab.
4. Paste EC2 read-only policy JSON.
5. Click Next.
6. Policy name: `iampolicy_jim`.
7. Create policy.

---

## Create EC2 Instance with Passwordless SSH
1. Open EC2 Dashboard.
2. Click Launch Instance.
3. Name the instance `devops-ec2`.
4. Select Amazon Linux AMI.
5. Select instance type `t2.micro`.
6. Configure security group to allow SSH.
7. Launch instance.
8. SSH into instance.
9. Add public key from `/root/.ssh/id_rsa.pub` to `/root/.ssh/authorized_keys`.
10. Test passwordless SSH from `aws-client`.

---

## Create S3 Bucket and Migrate Data
1. Open S3 Dashboard.
2. Click Create Bucket.
3. Bucket name: `xfusion-sync-15888`.
4. Keep Block Public Access enabled.
5. Create bucket.
6. Use AWS CLI to sync data:
```bash
aws s3 sync s3://xfusion-s3-25260 s3://xfusion-sync-15888
```
7. Verify using dry-run sync.

---

## Configure Application Load Balancer

### Create Security Group
1. Open EC2 Dashboard.
2. Go to Security Groups.
3. Create security group `xfusion-sg`.
4. Add inbound rule:
   - HTTP
   - Port 80
   - Source 0.0.0.0/0

### Create Target Group
1. Go to Target Groups.
2. Create target group `xfusion-tg`.
3. Protocol HTTP, Port 80.
4. Register instance `xfusion-ec2`.

### Create ALB
1. Go to Load Balancers.
2. Create Application Load Balancer.
3. Name: `xfusion-alb`.
4. Scheme: Internet-facing.
5. Select at least 2 subnets.
6. Attach security group `xfusion-sg`.
7. Configure listener:
   - HTTP
   - Port 80
   - Forward to `xfusion-tg`
8. Create Load Balancer.

### Update EC2 Security Group
1. Open EC2 Instance.
2. Open attached security group.
3. Edit inbound rules.
4. Allow HTTP port 80 from `xfusion-sg`.

---

## Fix ALB Availability Zone Issue
1. Open EC2 Dashboard.
2. Go to Load Balancers.
3. Select ALB.
4. Open Network Mapping tab.
5. Click Edit Subnets.
6. Add subnet from same AZ as EC2 instance.
7. Save changes.
8. Verify target becomes healthy.

---

# AWS Services Used

- Amazon EC2
- Amazon S3
- Elastic Load Balancing (ALB)
- IAM
- VPC
- Security Groups
- AMI
- ENI

---

# Author
Nahid Hasan

