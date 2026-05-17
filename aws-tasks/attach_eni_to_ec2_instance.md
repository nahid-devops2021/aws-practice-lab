# Attach ENI to EC2 Instance

### Task
Attach existing ENI `nautilus-eni` to EC2 instance `nautilus-ec2`.


### Attach ENI to EC2 Instance
1. Open EC2 Dashboard.
2. Go to Network Interfaces.
3. Select `nautilus-eni`.
4. Click Actions → Attach.
5. Select instance `nautilus-ec2`.
6. Set Device Index = 1.
7. Click Attach.
8. Verify status becomes `attached`.

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