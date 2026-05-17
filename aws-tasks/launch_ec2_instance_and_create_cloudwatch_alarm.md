# Launch EC2 Instance and Create CloudWatch Alarm

## Objective

- Launch an EC2 instance named `devops-ec2`
- Use Ubuntu AMI
- Create a CloudWatch alarm named `devops-alarm`
- Trigger alarm when CPU utilization exceeds 90% for 5 minutes
- Send notifications to SNS topic `devops-sns-topic`

---

## Launch EC2 Instance

### Steps

1. Open AWS Console
2. Navigate to:
   ```
   EC2 → Launch Instance
   ```
3. Configure:

| Field | Value |
|---|---|
| Name | devops-ec2 |
| AMI | Ubuntu Server |
| Instance Type | t2.micro |

4. Launch the instance

---

## Create CloudWatch Alarm

### Steps

1. Navigate to:
   ```
   CloudWatch → Alarms → Create Alarm
   ```
2. Select Metric:
   ```
   EC2 → Per-Instance Metrics → CPUUtilization
   ```
3. Configure Alarm:

| Setting | Value |
|---|---|
| Statistic | Average |
| Period | 5 minutes |
| Threshold | Greater than or equal to 90 |
| Evaluation Periods | 1 |

4. Configure Notification:

| Setting | Value |
|---|---|
| SNS Topic | devops-sns-topic |

5. Alarm Name:
   ```
   devops-alarm
   ```


