# AWS S3 Static Website Hosting Guide

---

# Task Requirements

- Create an S3 bucket named `datacenter-web-1128024934`
- Configure the bucket for static website hosting
- Use `index.html` as the index document
- Allow public access to the bucket
- Upload the `index.html` file from `/root/`
- Verify website accessibility using the S3 website URL

---

# Architecture Diagram

```text
                +----------------------+
                |   External Users     |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |  Amazon S3 Bucket    |
                | datacenter-web-*     |
                +----------------------+
                           |
                           v
                +----------------------+
                |      index.html      |
                +----------------------+
```

---

# Prerequisites

- AWS CLI installed and configured
- IAM user/role with S3 permissions
- `index.html` file available in `/root/`

Verify AWS CLI:

```bash
aws --version
```

Verify AWS identity:

```bash
aws sts get-caller-identity
```

---

# Step 1: Create the S3 Bucket

Create the bucket:

```bash
aws s3 mb s3://datacenter-web-1128024934
```

Verify bucket creation:

```bash
aws s3 ls
```

Expected output:

```text
2026-05-27  datacenter-web-1128024934
```

---

# Step 2: Disable Block Public Access

Amazon S3 blocks public access by default. Disable the block settings to make the website publicly accessible.

Run the following command:

```bash
aws s3api put-public-access-block \
  --bucket datacenter-web-1128024934 \
  --public-access-block-configuration \
  "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"
```

Verify:

```bash
aws s3api get-public-access-block \
  --bucket datacenter-web-1128024934
```

---

# Step 3: Enable Static Website Hosting

Configure the bucket for website hosting:

```bash
aws s3 website s3://datacenter-web-1128024934/ \
  --index-document index.html
```

Verify configuration:

```bash
aws s3api get-bucket-website \
  --bucket datacenter-web-1128024934
```

Expected output:

```json
{
  "IndexDocument": {
    "Suffix": "index.html"
  }
}
```

---

# Step 4: Create Public Read Bucket Policy

Create a policy file:

```bash
vi bucket-policy.json
```

Add the following content:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadAccess",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::datacenter-web-1128024934/*"
    }
  ]
}
```

Apply the bucket policy:

```bash
aws s3api put-bucket-policy \
  --bucket datacenter-web-1128024934 \
  --policy file://bucket-policy.json
```

Verify bucket policy:

```bash
aws s3api get-bucket-policy \
  --bucket datacenter-web-1128024934
```

---

# Step 5: Upload Website Files

Upload the `index.html` file:

```bash
aws s3 cp /root/index.html s3://datacenter-web-1128024934/
```

Verify uploaded files:

```bash
aws s3 ls s3://datacenter-web-1128024934/
```

Expected output:

```text
2026-05-27  index.html
```

---

# Step 6: Access the Static Website

Retrieve the website endpoint:

```bash
aws s3api get-bucket-location \
  --bucket datacenter-web-1128024934
```

Website endpoint format:

```text
http://datacenter-web-1128024934.s3-website-<region>.amazonaws.com
```

Example:

```text
http://datacenter-web-1128024934.s3-website-us-east-1.amazonaws.com
```

Test using curl:

```bash
curl http://datacenter-web-1128024934.s3-website-us-east-1.amazonaws.com
```

You should see the HTML content returned.

---

# AWS Console Configuration Steps

## Create Bucket

1. Open AWS Management Console
2. Navigate to S3
3. Click **Create bucket**
4. Enter bucket name:

```text
datacenter-web-1128024934
```

5. Uncheck:

```text
Block all public access
```

6. Acknowledge the warning
7. Click **Create bucket**

---

## Enable Static Website Hosting

1. Open the S3 bucket
2. Go to the **Properties** tab
3. Scroll to **Static website hosting**
4. Click **Edit**
5. Enable hosting
6. Set:

```text
Index document: index.html
```

7. Save changes

---

## Configure Bucket Policy

1. Open the **Permissions** tab
2. Navigate to **Bucket policy**
3. Paste the following policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadAccess",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::datacenter-web-1128024934/*"
    }
  ]
}
```

4. Save changes

---

## Upload Website File

1. Open the **Objects** tab
2. Click **Upload**
3. Select `/root/index.html`
4. Upload the file

---

## Access Website URL

1. Open the **Properties** tab
2. Scroll to **Static website hosting**
3. Open the generated website endpoint URL

---

# Validation Commands

Check bucket details:

```bash
aws s3 ls
```

Check uploaded objects:

```bash
aws s3 ls s3://datacenter-web-1128024934/
```

Check website configuration:

```bash
aws s3api get-bucket-website \
  --bucket datacenter-web-1128024934
```

Check public access block:

```bash
aws s3api get-public-access-block \
  --bucket datacenter-web-1128024934
```

---

# Troubleshooting

## Access Denied Error

Possible causes:

- Public access block still enabled
- Bucket policy missing
- Object permissions incorrect

Reapply the bucket policy and verify public access settings.

---

## Website Not Loading

Verify:

- `index.html` exists in the bucket
- Static website hosting is enabled
- Correct website endpoint URL is being used

---

# Cleanup Resources

Delete uploaded objects:

```bash
aws s3 rm s3://datacenter-web-1128024934 --recursive
```

Delete the bucket:

```bash
aws s3 rb s3://datacenter-web-1128024934
```

---

# Expected Outcome

After successful completion:

- S3 bucket is publicly accessible
- Static website hosting is enabled
- `index.html` loads successfully in a browser
- Website is accessible via the S3 website endpoint URL

---

# Useful References

- AWS S3 Documentation: https://docs.aws.amazon.com/s3/
- Static Website Hosting: https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html
- AWS CLI S3 Reference: https://docs.aws.amazon.com/cli/latest/reference/s3/

