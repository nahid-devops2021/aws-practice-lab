# AWS RDS Snapshot and Restore Runbook

## Objective

As a member of the Nautilus DevOps Team, perform the following tasks:

1. Take a snapshot of the existing RDS instance `nautilus-rds`
2. Name the snapshot `nautilus-snapshot`
3. Restore the snapshot to a new RDS instance named `nautilus-snapshot-restore`
4. Configure the restored RDS instance with class `db.t3.micro`
5. Verify the restored instance is in `Available` state

---

# Prerequisites

- AWS Console access
- Required IAM permissions:
  - AmazonRDSFullAccess (or equivalent custom permissions)
- Existing RDS instance:
  - `nautilus-rds`

---

# AWS Console Steps

## Step 1: Open AWS RDS Console

1. Login to the AWS Management Console.
2. Search for **RDS**.
3. Open the RDS Dashboard.

---

## Step 2: Verify Source RDS Status

1. From the left navigation menu click:
   - **Databases**
2. Select the database:
   - `nautilus-rds`
3. Verify the database status is:

```text
Available
```

> Wait until the RDS instance becomes available before proceeding.

---

## Step 3: Create Snapshot

1. Select the database:
   - `nautilus-rds`
2. Click:
   - **Actions**
3. Select:
   - **Take snapshot**

---

## Step 4: Configure Snapshot

Provide the following snapshot identifier:

```text
nautilus-snapshot
```

Click:

```text
Take snapshot
```

---

## Step 5: Wait for Snapshot Completion

1. Navigate to:
   - **Snapshots**
2. Locate the snapshot:
   - `nautilus-snapshot`
3. Wait until the snapshot status changes to:

```text
Available
```

---

## Step 6: Restore Snapshot

1. Select the snapshot:
   - `nautilus-snapshot`
2. Click:
   - **Actions**
3. Select:
   - **Restore snapshot**

---

## Step 7: Configure Restored RDS Instance

### DB Instance Identifier

Set the following value:

```text
nautilus-snapshot-restore
```

### DB Instance Class

Select:

```text
db.t3.micro
```

---

## Step 8: Configure Remaining Settings

Keep the remaining configuration as default unless your environment requires custom values:

- VPC
- Subnet Group
- Security Group
- Storage
- Backup Configuration
- Monitoring

---

## Step 9: Restore Database Instance

Click:

```text
Restore DB instance
```

AWS will begin provisioning the restored RDS instance.

---

## Step 10: Verify Restored Instance

1. Navigate to:
   - **Databases**
2. Locate:
   - `nautilus-snapshot-restore`

Verify the following:

| Parameter | Expected Value |
|---|---|
| DB Instance Identifier | nautilus-snapshot-restore |
| DB Instance Class | db.t3.micro |
| Status | Available |

---

# AWS CLI Commands (Optional)

## Verify RDS Status

```bash
aws rds describe-db-instances \
  --db-instance-identifier nautilus-rds \
  --query "DBInstances[0].DBInstanceStatus"
```

---

## Create Snapshot

```bash
aws rds create-db-snapshot \
  --db-instance-identifier nautilus-rds \
  --db-snapshot-identifier nautilus-snapshot
```

---

## Wait for Snapshot Completion

```bash
aws rds wait db-snapshot-available \
  --db-snapshot-identifier nautilus-snapshot
```

---

## Restore Snapshot

```bash
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier nautilus-snapshot-restore \
  --db-snapshot-identifier nautilus-snapshot \
  --db-instance-class db.t3.micro
```

---

## Wait for Restored Instance

```bash
aws rds wait db-instance-available \
  --db-instance-identifier nautilus-snapshot-restore
```

---

# Validation Checklist

- [ ] Source RDS instance `nautilus-rds` is available
- [ ] Snapshot `nautilus-snapshot` created successfully
- [ ] Snapshot status is `Available`
- [ ] Restored RDS instance `nautilus-snapshot-restore` created successfully
- [ ] Restored instance class is `db.t3.micro`
- [ ] Restored instance status is `Available`

---

# Expected Outcome

The following resources should exist successfully:

| Resource Type | Resource Name |
|---|---|
| RDS Snapshot | nautilus-snapshot |
| Restored RDS Instance | nautilus-snapshot-restore |

The restored RDS instance must remain in:

```text
Available
```

state after the restoration process is completed.

