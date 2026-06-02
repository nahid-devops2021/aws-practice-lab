# 5. Create IAM Policy

### Task
Create IAM policy `iampolicy_jim` with EC2 read-only access.

### Policy JSON
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeImages",
        "ec2:DescribeSnapshots",
        "ec2:DescribeVolumes",
        "ec2:DescribeSecurityGroups",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DescribeTags",
        "ec2:DescribeRegions",
        "ec2:DescribeAvailabilityZones"
      ],
      "Resource": "*"
    }
  ]
}
```

### Create Policy
```bash
aws iam create-policy \
  --policy-name iampolicy_jim \
  --policy-document file://ec2-readonly.json
```

---

## Create IAM Policy
1. Open IAM Dashboard.
2. Click Policies → Create Policy.
3. Open JSON tab.
4. Paste EC2 read-only policy JSON.
5. Click Next.
6. Policy name: `iampolicy_jim`.
7. Create policy.