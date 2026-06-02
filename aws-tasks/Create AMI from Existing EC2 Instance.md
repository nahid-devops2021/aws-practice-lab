---
# Create AMI from Existing EC2 Instance

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

## Create AMI from Existing EC2 Instance
1. Open EC2 Dashboard.
2. Select instance `nautilus-ec2`.
3. Click Actions → Image and Templates → Create Image.
4. Enter AMI name: `nautilus-ec2-ami`.
5. Click Create Image.
6. Go to AMIs section.
7. Wait until status becomes `available`.