# Configure Application Load Balancer

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



# ALB Troubleshooting

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