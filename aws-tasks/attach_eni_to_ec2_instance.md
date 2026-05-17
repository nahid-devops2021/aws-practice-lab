# Attach ENI to EC2 Instance

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