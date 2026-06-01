# Create a Private Amazon EKS Cluster (`xfusion-eks`)

## Objective
Create an Amazon EKS cluster with the following requirements:

- Cluster Name: `xfusion-eks`
- Use the latest stable Kubernetes version
- Use IAM Role: `eksClusterRole`
- Disable EKS Auto Mode
- Endpoint Access: **Private**
- Use the **default VPC**
- Use Availability Zones:
  - `a`
  - `b`
  - `c`
- Verify the cluster is active and ready for workloads

---

# Architecture Overview

```text
                +---------------------------+
                |      Amazon EKS Cluster   |
                |       xfusion-eks         |
                +---------------------------+
                           |
         -----------------------------------------
         |                  |                    |
+----------------+ +----------------+ +----------------+
| Subnet AZ-a    | | Subnet AZ-b    | | Subnet AZ-c    |
| Default VPC    | | Default VPC    | | Default VPC    |
+----------------+ +----------------+ +----------------+

Endpoint Access: Private Only
IAM Role: eksClusterRole
EKS Auto Mode: Disabled
```

---

# Step 1: Verify IAM Role

Verify that the IAM role `eksClusterRole` exists.

## AWS Console

1. Open AWS Console
2. Navigate to:

```text
IAM → Roles
```

3. Search for:

```text
eksClusterRole
```

4. Ensure the following policy is attached:

```text
AmazonEKSClusterPolicy
```

---

# Step 2: Create EKS Cluster Using AWS Console

## Open EKS Service

Navigate to:

```text
Amazon EKS → Clusters → Create Cluster
```

---

## Basic Configuration

| Field | Value |
|---|---|
| Cluster Name | `xfusion-eks` |
| Kubernetes Version | Latest Stable Version |
| Cluster IAM Role | `eksClusterRole` |

Click:

```text
Next
```

---

# Step 3: Networking Configuration

## Select Default VPC

Choose the default VPC.

### Select Subnets

Choose subnets from:

- Availability Zone `a`
- Availability Zone `b`
- Availability Zone `c`

Example:

| Availability Zone | Example Subnet |
|---|---|
| us-east-1a | subnet-xxxxa |
| us-east-1b | subnet-xxxxb |
| us-east-1c | subnet-xxxxc |

---

## Endpoint Access Configuration

Set:

| Setting | Value |
|---|---|
| Public Access | Disabled |
| Private Access | Enabled |

This ensures the EKS API server is accessible only within the VPC.

Click:

```text
Next
```

---

# Step 4: Configure Cluster Access

Leave default settings unless otherwise required.

Click:

```text
Next
```

---

# Step 5: Configure Add-ons

Keep default add-ons.

Click:

```text
Next
```

---

# Step 6: Configure EKS Auto Mode

Disable:

```text
EKS Auto Mode
```

Ensure:

| Setting | Value |
|---|---|
| EKS Auto Mode | Disabled |

Click:

```text
Next
```

---

# Step 7: Review and Create

Review all configurations.

Click:

```text
Create
```

Cluster creation may take several minutes.

---

# AWS CLI Method

## Step 1: Get Default VPC ID

```bash
aws ec2 describe-vpcs \
  --filters "Name=isDefault,Values=true" \
  --query 'Vpcs[0].VpcId' \
  --output text
```

Example Output:

```text
vpc-1234567890abcdef0
```

---

## Step 2: Get Subnet IDs from AZ a, b, c

```bash
aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=vpc-1234567890abcdef0" \
  --query 'Subnets[*].[SubnetId,AvailabilityZone]' \
  --output table
```

Select one subnet from each AZ:

- `a`
- `b`
- `c`

Example:

```text
subnet-aaa111
subnet-bbb222
subnet-ccc333
```

---

## Step 3: Create EKS Cluster

```bash
aws eks create-cluster \
  --name xfusion-eks \
  --role-arn arn:aws:iam::<ACCOUNT_ID>:role/eksClusterRole \
  --resources-vpc-config subnetIds=subnet-aaa111,subnet-bbb222,subnet-ccc333,endpointPublicAccess=false,endpointPrivateAccess=true \
  --kubernetes-version <LATEST_VERSION>
```

Replace:

- `<ACCOUNT_ID>` with your AWS Account ID
- `<LATEST_VERSION>` with the latest supported EKS version

Example:

```bash
aws eks create-cluster \
  --name xfusion-eks \
  --role-arn arn:aws:iam::123456789012:role/eksClusterRole \
  --resources-vpc-config subnetIds=subnet-aaa111,subnet-bbb222,subnet-ccc333,endpointPublicAccess=false,endpointPrivateAccess=true \
  --kubernetes-version 1.33
```

---

# Step 4: Verify Cluster Creation

## Check Cluster Status

```bash
aws eks describe-cluster \
  --name xfusion-eks \
  --query 'cluster.status' \
  --output text
```

Expected Output:

```text
ACTIVE
```

---

# Step 5: Verify Endpoint Access

```bash
aws eks describe-cluster \
  --name xfusion-eks \
  --query 'cluster.resourcesVpcConfig'
```

Expected Values:

```json
{
  "endpointPublicAccess": false,
  "endpointPrivateAccess": true
}
```

---

# Step 6: Verify Kubernetes Version

```bash
aws eks describe-cluster \
  --name xfusion-eks \
  --query 'cluster.version' \
  --output text
```

---

# Step 7: Update kubeconfig

```bash
aws eks update-kubeconfig \
  --name xfusion-eks \
  --region <REGION>
```

Example:

```bash
aws eks update-kubeconfig \
  --name xfusion-eks \
  --region us-east-1
```

---

# Step 8: Verify Cluster Connectivity

```bash
kubectl get nodes
```

If worker nodes are not yet attached, the output may show:

```text
No resources found
```

The control plane is still considered active and ready.

---

# Final Verification Checklist

| Verification | Status |
|---|---|
| Cluster Name = xfusion-eks | ✅ |
| Latest Kubernetes Version Used | ✅ |
| IAM Role = eksClusterRole | ✅ |
| Default VPC Used | ✅ |
| Subnets in AZ a,b,c | ✅ |
| Endpoint Access = Private | ✅ |
| Public Endpoint Disabled | ✅ |
| EKS Auto Mode Disabled | ✅ |
| Cluster Status = ACTIVE | ✅ |

---

# Useful Commands

## List EKS Clusters

```bash
aws eks list-clusters
```

---

## Get Cluster Details

```bash
aws eks describe-cluster --name xfusion-eks
```

---

## Delete Cluster

```bash
aws eks delete-cluster --name xfusion-eks
```

---

# Notes

- Private endpoint access means kubectl access works only from inside the VPC or connected network.
- Ensure security groups and routing allow internal communication.
- Worker nodes or managed node groups can be added later.
- EKS Auto Mode remains disabled as required.

