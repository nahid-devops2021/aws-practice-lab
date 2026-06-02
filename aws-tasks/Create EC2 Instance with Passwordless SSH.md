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