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
