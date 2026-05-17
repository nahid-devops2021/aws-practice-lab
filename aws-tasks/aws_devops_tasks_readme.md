

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

