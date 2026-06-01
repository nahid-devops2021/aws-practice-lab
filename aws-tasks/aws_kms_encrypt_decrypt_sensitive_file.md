# AWS KMS Encryption and Decryption Guide

## Overview

The Nautilus DevOps team needs to improve data security using AWS Key Management Service (KMS). This guide explains how to:

- Create a symmetric AWS KMS key
- Encrypt a sensitive file using the KMS key
- Base64 encode the encrypted output
- Decrypt and verify the file contents
- Validate successful encryption and decryption

---

# Task Objective

Perform the following tasks:

1. Create a symmetric KMS key named:

```text
nautilus-KMS-Key
```

2. Encrypt the file:

```text
/root/SensitiveData.txt
```

3. Base64 encode the ciphertext and save it as:

```text
/root/EncryptedData.bin
```

4. Decrypt the encrypted file and verify the contents match the original file.

---

# Architecture Overview

```text
SensitiveData.txt
        │
        ▼
AWS KMS Key (nautilus-KMS-Key)
        │
        ▼
Encrypted Ciphertext
        │
        ▼
Base64 Encoding
        │
        ▼
EncryptedData.bin
        │
        ▼
KMS Decryption
        │
        ▼
Original Plaintext
```

---

# Prerequisites

Ensure the following:

- AWS CLI is installed
- AWS CLI is configured with valid credentials
- IAM permissions allow KMS operations
- File exists:

```text
/root/SensitiveData.txt
```

Verify:

```bash
ls -l /root/SensitiveData.txt
```

---

# AWS Console Steps

## Step 1: Login to AWS Console

Open:

```text
https://console.aws.amazon.com/
```

Login using your AWS account credentials.

---

## Step 2: Open AWS KMS Service

Search for:

```text
KMS
```

Open:

```text
Key Management Service (KMS)
```

---

## Step 3: Create Symmetric KMS Key

Navigate:

```text
KMS → Customer managed keys
```

Click:

```text
Create key
```

---

### Configure Key Type

Select:

```text
Symmetric
```

### Configure Key Usage

Select:

```text
Encrypt and decrypt
```

Click:

```text
Next
```

---

## Step 4: Configure Alias

Enter alias:

```text
nautilus-KMS-Key
```

Optional description:

```text
KMS key for sensitive file encryption
```

Click:

```text
Next
```

---

## Step 5: Configure Key Administrators

Select the IAM users or roles that can administer the key.

Click:

```text
Next
```

---

## Step 6: Configure Key Usage Permissions

Select IAM users or roles allowed to:

- Encrypt
- Decrypt

Click:

```text
Next
```

---

## Step 7: Review and Create Key

Review all configurations.

Click:

```text
Finish
```

---

## Step 8: Verify KMS Key Creation

Navigate:

```text
KMS → Customer managed keys
```

Verify:

| Setting | Expected Value |
|---------|----------------|
| Alias | nautilus-KMS-Key |
| Key Type | Symmetric |
| Key Usage | Encrypt and decrypt |
| Status | Enabled |

---

## Step 9: Connect to EC2 Instance

Navigate:

```text
EC2 → Instances
```

Select the instance.

Click:

```text
Connect
```

Use either:

- EC2 Instance Connect
- SSH Client

---

# AWS CLI Steps

## Step 1: Create AWS KMS Key

Run the following command:

```bash
aws kms create-key \
--description "nautilus-KMS-Key" \
--key-usage ENCRYPT_DECRYPT \
--customer-master-key-spec SYMMETRIC_DEFAULT
```

Expected Output:

```json
{
  "KeyMetadata": {
    "KeyId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  }
}
```

Save the `KeyId` value.

Example:

```text
1234abcd-12ab-34cd-56ef-1234567890ab
```

---

# Step 2: Create Alias for KMS Key

Create the alias:

```bash
aws kms create-alias \
--alias-name alias/nautilus-KMS-Key \
--target-key-id KEY_ID
```

Example:

```bash
aws kms create-alias \
--alias-name alias/nautilus-KMS-Key \
--target-key-id 1234abcd-12ab-34cd-56ef-1234567890ab
```

---

# Step 3: Encrypt Sensitive File

Run the following command:

```bash
aws kms encrypt \
--key-id alias/nautilus-KMS-Key \
--plaintext fileb:///root/SensitiveData.txt \
--query CiphertextBlob \
--output text > /root/EncryptedData.bin
```

---

# Explanation

| Option | Purpose |
|--------|---------|
| `--key-id` | Specifies the KMS key |
| `fileb://` | Reads plaintext file in binary mode |
| `CiphertextBlob` | Returns encrypted ciphertext |
| `--output text` | Outputs base64 encoded ciphertext |
| `>` | Saves output to file |

---

# Important Note

Do NOT use:

```bash
| base64 --decode
```

while encrypting.

AWS KMS already returns the ciphertext in base64 encoded format when using:

```bash
--output text
```

Using additional base64 decoding during encryption will convert the ciphertext into binary data and may fail validation requirements.

---

# Step 4: Verify Encrypted File

Check the encrypted file:

```bash
cat /root/EncryptedData.bin
```

Expected:

- Base64 encoded encrypted content
- Unreadable ciphertext

---

# Step 5: Decrypt the Encrypted File

Run the following command:

```bash
aws kms decrypt \
--ciphertext-blob fileb://<(base64 --decode /root/EncryptedData.bin) \
--query Plaintext \
--output text | base64 --decode > /root/DecryptedData.txt
```

---

# Explanation

| Option | Purpose |
|--------|---------|
| `base64 --decode` | Decodes encrypted base64 ciphertext |
| `CiphertextBlob` | Sends ciphertext to KMS |
| `Plaintext` | Returns decrypted data |
| `--output text` | Outputs base64 plaintext |
| `base64 --decode` | Converts plaintext back to readable text |

---

# Important Notes

## Query Field is Case-Sensitive

Correct:

```bash
--query Plaintext
```

Incorrect:

```bash
--query plaintext
```

Using lowercase `plaintext` may produce invalid output.

---

## Why Base64 Decode During Decryption?

The encrypted file contains base64 encoded ciphertext.

Before decryption, the ciphertext must be decoded back into binary format using:

```bash
base64 --decode
```

---

# Step 6: Verify Decrypted Content

Compare original and decrypted files:

```bash
diff /root/SensitiveData.txt /root/DecryptedData.txt
```

Expected Result:

```text
(no output)
```

No output means both files are identical.

---

# Additional Verification

## View KMS Key Details

```bash
aws kms list-keys
```

---

## Describe Key

```bash
aws kms describe-key \
--key-id alias/nautilus-KMS-Key
```

---

## List Aliases

```bash
aws kms list-aliases
```

---

# Complete Workflow Example

## Create Key

```bash
aws kms create-key \
--description "nautilus-KMS-Key" \
--key-usage ENCRYPT_DECRYPT \
--customer-master-key-spec SYMMETRIC_DEFAULT
```

---

## Create Alias

```bash
aws kms create-alias \
--alias-name alias/nautilus-KMS-Key \
--target-key-id KEY_ID
```

---

## Encrypt File

```bash
aws kms encrypt \
--key-id alias/nautilus-KMS-Key \
--plaintext fileb:///root/SensitiveData.txt \
--query CiphertextBlob \
--output text > /root/EncryptedData.bin
```

---

## Decrypt File

```bash
aws kms decrypt \
--ciphertext-blob fileb://<(base64 -d /root/EncryptedData.bin) \
--query Plaintext \
--output text | base64 -d > /root/DecryptedData.txt
```

---

## Verify Integrity

```bash
diff /root/SensitiveData.txt /root/DecryptedData.txt
```

---

# Important Notes

## Symmetric Key Requirement

The task specifically requires a symmetric KMS key.

Required specification:

```text
SYMMETRIC_DEFAULT
```

---

## Why Base64 Encoding?

AWS KMS returns encrypted ciphertext in binary format.

Using:

```text
--output text
```

returns a base64 encoded version suitable for storage in:

```text
/root/EncryptedData.bin
```

---

# Common Issues and Solutions

| Problem | Solution |
|---------|-----------|
| AccessDeniedException | Verify IAM KMS permissions |
| InvalidCiphertextException | Ensure correct base64 decoding |
| Alias already exists | Delete existing alias or use another |
| File not found | Verify SensitiveData.txt exists |
| Incorrect key type | Use SYMMETRIC_DEFAULT |

---

# Required IAM Permissions

Example IAM permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "kms:CreateKey",
        "kms:Encrypt",
        "kms:Decrypt",
        "kms:DescribeKey",
        "kms:CreateAlias",
        "kms:ListKeys",
        "kms:ListAliases"
      ],
      "Resource": "*"
    }
  ]
}
```

---

# Validation Checklist

| Task | Status |
|------|---------|
| Symmetric KMS key created | ✅ |
| Alias configured | ✅ |
| Sensitive file encrypted | ✅ |
| Ciphertext stored in EncryptedData.bin | ✅ |
| File successfully decrypted | ✅ |
| Decrypted content verified | ✅ |

---

# Final Result

After completing the above steps:

- AWS KMS securely manages encryption keys.
- Sensitive data is encrypted using the symmetric KMS key.
- Encrypted ciphertext is safely stored.
- The encrypted file can be successfully decrypted and validated.
- The validation script will be able to decrypt `EncryptedData.bin` using the configured KMS key.

---

# Conclusion

This implementation demonstrates secure file encryption and decryption using AWS KMS best practices.

Using AWS KMS provides:

- Centralized key management
- Secure encryption operations
- Controlled access via IAM
- Auditability through AWS CloudTrail
- Enterprise-grade data protection

