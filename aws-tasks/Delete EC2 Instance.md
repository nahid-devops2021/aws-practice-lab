---
Delete EC2 Instance

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

## Delete EC2 Instance
1. Open EC2 Dashboard.
2. Select instance `datacenter-ec2`.
3. Click Instance State → Terminate Instance.
4. Confirm termination.
5. Wait until instance state becomes `terminated`.