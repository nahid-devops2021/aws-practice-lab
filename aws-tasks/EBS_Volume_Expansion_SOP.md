# SOP: Online EBS Volume Expansion for `nautilus-ec2`

This Standard Operating Procedure (SOP) outlines the steps required to safely expand the EBS root volume of the `nautilus-ec2` instance from **8 GiB to 12 GiB** and reflect those changes in the live OS file system without causing any service disruption or downtime.

---

## 📋 Prerequisites & Infrastructure Information

*   **Instance Name:** `nautilus-ec2`
*   **Initial Volume Size:** 8 GiB
*   **Target Volume Size:** 12 GiB
*   **SSH Key Pair Location:** `/root/nautilus-keypair.pem` (stored on the `aws-client` host)
*   **Goal:** Zero downtime expansion of the root (`/`) partition.

---

## 🛠️ Step-by-Step Implementation

### Step 1: Expand the EBS Volume via AWS

Before modifying the operating system partitions, the block storage capacity must be increased on the AWS side.

#### Option A: Via AWS Management Console
1. Navigate to the **Amazon EC2 Console**.
2. From the left sidebar, click **Instances** and select `nautilus-ec2`.
3. Open the **Storage** tab in the bottom pane and click on the **Volume ID** attached to the root device (e.g., `/dev/xvda` or `/dev/sda1`).
4. Select the checked volume, click **Actions** ➔ **Modify volume**.
5. Update the **Size** field from `8` to `12`.
6. Click **Modify** and confirm the prompt.

#### Option B: Via AWS CLI (From `aws-client`)
If you have administrative access to the AWS CLI on your client machine, find the volume ID and execute:
```bash
aws ec2 modify-volume --volume-id <VOLUME_ID> --size 12
```

> ⏳ **Note:** Wait for the volume state to transition from `modifying` to `optimizing` or `completed` before continuing to the OS configuration steps. This process happens in the background and does not affect disk performance.

---

### Step 2: Establish SSH Access to the Instance

Log in to the `aws-client` host where the infrastructure deployment private key is located, correct its permissions, and SSH into the target machine.

```bash
# 1. Secure the private key permissions
chmod 400 /root/nautilus-keypair.pem

# 2. SSH into nautilus-ec2 (replace <USER> and <IP> with your target values)
# Default users: 'ec2-user' (Amazon Linux), 'ubuntu' (Ubuntu), 'centos' (CentOS)
ssh -i /root/nautilus-keypair.pem <USER>@<NAUTILUS_EC2_IP>
```

---

### Step 3: Extend the Partition

Once inside `nautilus-ec2`, verify that the system registers the block device's new physical size, then grow the target partition block.

#### 1. Inspect the Block Storage Block layout
Run `lsblk` to view the storage architecture:
```bash
lsblk
```

*Example Expected Output:*
```text
NAME    MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
nvme0n1 259:0    0   12G  0 disk             <-- OS sees physical 12G allocation
└─nvme0n1p1
        259:1    0    8G  0 part /            <-- Root partition is trapped at 8G
```

#### 2. Grow the Partition Block
Use the `growpart` utility to expand the partition structure. 

> ⚠️ **Syntax Warning:** There is a mandatory space character between the disk name and the partition number.

*   **For NVMe Disks (Modern instance types like t3, c5, m5):**
    ```bash
    sudo growpart /dev/nvme0n1 1
    ```
*   **For Xen / Legacy Disks (Older instance types like t2):**
    ```bash
    sudo growpart /dev/xvda 1
    ```

*Verify the structural change:*
```bash
lsblk
```
The partition (e.g., `nvme0n1p1`) should now reflect the updated capacity of `12G`.

---

### Step 4: Resize the File System Layer

The partition structure is now 12 GiB, but the file system inside it is still unaware of the new space. You must expand the file system to consume the newly allocated boundary blocks.

#### 1. Identify File System Type
Run the following to check if the root filesystem is `XFS` or `Ext4`:
```bash
df -T /
```

#### 2. Execute the Targeted Resize Command
Depending on the **Type** column output from the command above, choose the matching utility:

*   **If File System Type is `xfs`:**
    ```bash
    sudo xfs_growfs -d /
    ```
*   **If File System Type is `ext4`:**
    ```bash
    # For NVMe layout:
    sudo resize2fs /dev/nvme0n1p1
    
    # For Legacy/Xen layout:
    sudo resize2fs /dev/xvda1
    ```

---

## 🏁 Step 5: Post-Expansion Verification

Confirm that the operating system root logical mount path acknowledges the expanded volume matrix:

```bash
df -h /
```

*Expected Final Verification Output:*
```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p1   12G  7.1G  4.9G  60% /
```

The `nautilus-ec2` volume expansion is complete, and the additional 4 GiB space is fully accessible for the development team without any service interruption.
