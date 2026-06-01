# AWS NAT Gateway Setup for Private EC2 Internet Access

## Architecture

```
Internet
    |
    v
Internet Gateway
    |
Public Subnet (datacenter-pub-subnet)
    |
NAT Gateway (datacenter-natgw)
    |
Private Route Table
    |
Private Subnet (datacenter-priv-subnet)
    |
EC2 Instance (datacenter-priv-ec2)
```

---

## Step 1: Verify Existing Resources

Navigate to **VPC Console** and confirm the following resources exist:

| Resource        | Name                    |
|----------------|------------------------|
| VPC            | datacenter-priv-vpc     |
| Private Subnet | datacenter-priv-subnet  |
| EC2 Instance   | datacenter-priv-ec2     |

---

## Step 2: Create Public Subnet

Go to **VPC → Subnets → Create subnet**

| Setting        | Value                        |
|----------------|-----------------------------|
| VPC            | datacenter-priv-vpc          |
| Subnet Name    | datacenter-pub-subnet        |
| AZ             | Same AZ as private subnet    |
| IPv4 CIDR      | 10.0.2.0/24 (example)        |

Click **Create subnet**.

---

## Step 3: Enable Auto-Assign Public IP

Select `datacenter-pub-subnet`:

- Actions → Edit subnet settings
- Enable **Auto-assign public IPv4 address**
- Save

---

## Step 4: Create Internet Gateway

Go to **VPC → Internet Gateways → Create internet gateway**

| Setting | Value              |
|----------|-------------------|
| Name     | datacenter-igw    |

Click **Create Internet Gateway**.

---

## Step 5: Attach Internet Gateway

Select `datacenter-igw`:

- Actions → Attach to VPC
- Select `datacenter-priv-vpc`
- Click **Attach**

---

## Step 6: Create Public Route Table

Go to **VPC → Route Tables → Create route table**

| Setting | Value                 |
|----------|----------------------|
| Name     | datacenter-pub-rt    |
| VPC      | datacenter-priv-vpc  |

Click **Create**.

---

## Step 7: Add Internet Route

Open `datacenter-pub-rt` → Routes → Edit routes

| Destination | Target              |
|-------------|---------------------|
| 0.0.0.0/0   | Internet Gateway    |

Save changes.

---

## Step 8: Associate Public Subnet

Open `datacenter-pub-rt`:

- Subnet Associations → Edit associations
- Select `datacenter-pub-subnet`
- Save

---

## Step 9: Allocate Elastic IP

Go to **EC2 → Elastic IPs**

- Click **Allocate Elastic IP**
- Leave defaults
- Click **Allocate**

Note the Elastic IP.

---

## Step 10: Create NAT Gateway

Go to **VPC → NAT Gateways → Create NAT Gateway**

| Setting           | Value                    |
|------------------|--------------------------|
| Name             | datacenter-natgw         |
| Subnet           | datacenter-pub-subnet    |
| Connectivity Type | Public                   |
| Elastic IP       | Select allocated EIP     |

Click **Create NAT Gateway**.

Wait until status becomes **Available**.

---

## Step 11: Update Private Route Table

Open route table associated with `datacenter-priv-subnet`

Edit routes:

| Destination | Target               |
|-------------|----------------------|
| 0.0.0.0/0   | NAT Gateway          |

Save changes.

Final route table:

| Destination | Target         |
|-------------|---------------|
| VPC CIDR    | local         |
| 0.0.0.0/0   | NAT Gateway   |

---

## Step 12: Verify Internet Connectivity

Wait **2–3 minutes**.

The EC2 instance `datacenter-priv-ec2` should now be able to access the internet and upload a test file to:

```
datacenter-nat-745994107
```

---

## Step 13: Verify S3 Upload

Go to **S3 Console → datacenter-nat-745994107**

Refresh after a few minutes.

You should see a newly uploaded file confirming:

- NAT Gateway is working
- Private EC2 has outbound internet access
- S3 upload is successful

---

## Optional CLI Verification

If connected via Session Manager:

```bash
curl https://checkip.amazonaws.com
```

Expected output:

- Public IP (NAT Gateway Elastic IP)

This confirms outbound traffic is routed through NAT Gateway.

