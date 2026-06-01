# AWS Auto Scaling Group + Application Load Balancer Setup

## Resources
- Launch Template: `nautilus-launch-template`
- Auto Scaling Group: `nautilus-asg`
- Target Group: `nautilus-tg`
- Application Load Balancer: `nautilus-alb`

## Launch Template

### AMI
Amazon Linux 2

### Instance Type
`t2.micro`

### User Data
```bash
#!/bin/bash
yum update -y
amazon-linux-extras install nginx1 -y

systemctl start nginx
systemctl enable nginx

echo "<h1>Nautilus Auto Scaling Web Server</h1>" > /usr/share/nginx/html/index.html
```

## Auto Scaling Group

| Setting | Value |
|----------|--------|
| Desired Capacity | 1 |
| Minimum Capacity | 1 |
| Maximum Capacity | 2 |

### Target Tracking Policy
- Metric: Average CPU Utilization
- Target Value: 50%

## Target Group
- Name: `nautilus-tg`
- Protocol: HTTP
- Port: 80
- Health Check Path: `/`

## Application Load Balancer
- Name: `nautilus-alb`
- Listener: HTTP:80
- Scheme: Internet-facing
- Forward traffic to: `nautilus-tg`

## Security Groups

### ALB Security Group
Inbound:
- HTTP (80) from `0.0.0.0/0`

### EC2 Security Group
Inbound:
- HTTP (80) from ALB Security Group

## Verification

1. Verify EC2 instance is running.
2. Verify target health is `healthy`.
3. Obtain ALB DNS name.
4. Open the ALB DNS URL in a browser.
5. Confirm the Nginx page is displayed.

## Important

The Auto Scaling Group must be configured as:

```text
Desired Capacity = 1
Minimum Capacity = 1
Maximum Capacity = 2
Target CPU Utilization = 50%
```

If Maximum Capacity is set to 1, Auto Scaling cannot launch a second instance.
