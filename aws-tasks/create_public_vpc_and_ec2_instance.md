# Create Public VPC and EC2 Instance

## Objective

- Create public VPC `xfusion-pub-vpc`
- Create subnet `xfusion-pub-subnet`
- Enable auto public IP assignment
- Launch EC2 instance `xfusion-pub-ec2`
- Allow SSH access over internet

---

## Create VPC

| Field | Value |
|---|---|
| Name | xfusion-pub-vpc |
| CIDR | 10.0.0.0/16 |

---

## Create Public Subnet

| Field | Value |
|---|---|
| Name | xfusion-pub-subnet |
| CIDR | 10.0.1.0/24 |

Enable:

```
Auto-assign public IPv4 address
```

---

## Create Internet Gateway

| Field | Value |
|---|---|
| Name | xfusion-igw |

Attach internet gateway to:

```
xfusion-pub-vpc
```

---

## Configure Route Table

### Route

| Destination | Target |
|---|---|
| 0.0.0.0/0 | Internet Gateway |

Associate route table with:

```
xfusion-pub-subnet
```

---

## Create Security Group

| Type | Port | Source |
|---|---|---|
| SSH | 22 | 0.0.0.0/0 |

---

## Launch EC2 Instance

| Field | Value |
|---|---|
| Name | xfusion-pub-ec2 |
| Instance Type | t2.micro |
| VPC | xfusion-pub-vpc |
| Subnet | xfusion-pub-subnet |

Enable:

```
Auto-assign Public IP
```






