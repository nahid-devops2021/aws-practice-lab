# EC2 Instance with Nginx Using User Data

## Objective

- Create EC2 instance named `nautilus-ec2`
- Use Ubuntu AMI
- Install and start Nginx using user data script
- Allow HTTP traffic on port 80

---

## Launch EC2 Instance

### Configuration

| Field | Value |
|---|---|
| Name | nautilus-ec2 |
| AMI | Ubuntu Server |
| Instance Type | t2.micro |

---

## Security Group Rules

| Type | Port | Source |
|---|---|---|
| SSH | 22 | Your IP |
| HTTP | 80 | 0.0.0.0/0 |

---

## User Data Script

```bash
#!/bin/bash
apt update -y
apt install nginx -y
systemctl start nginx
systemctl enable nginx
```

