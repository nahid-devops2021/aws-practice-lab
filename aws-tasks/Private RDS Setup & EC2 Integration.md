📘 Nautilus DevOps – Private RDS Setup & EC2 Integration
🧭 Overview

The Nautilus DevOps team requires a secure and private MySQL RDS database integrated with an existing EC2 instance (nautilus-ec2). This setup ensures secure backend connectivity and application hosting via Apache + PHP.

🏗️ Architecture
EC2 Instance: nautilus-ec2 (Web Server)
RDS Instance: nautilus-rds (MySQL 8.4.5, private)
Database Name: nautilus_db
Connectivity: EC2 → RDS via Security Group (Port 3306)
Web Access: Public via EC2 (Port 80)
🚀 1. Create RDS MySQL Instance
🔹 AWS Console Steps

Navigate:
👉 RDS → Create database

Configuration
Parameter	Value
Engine	MySQL
Version	8.4.5
Template	Sandbox
DB Identifier	nautilus-rds
Instance Class	db.t3.micro
Storage Type	gp2
Storage Size	5 GiB
DB Name	nautilus_db
Username	nautilus_admin
Password	(secure password)
Networking
VPC: Same as EC2
Public Access: ❌ Disabled
Security Group: nautilus-rds-sg
🔐 2. Security Group Configuration
🔸 RDS Security Group (nautilus-rds-sg)

Inbound Rule:

Type	Port	Source
MySQL/Aurora	3306	nautilus-ec2-sg
🔸 EC2 Security Group (nautilus-ec2-sg)

Inbound Rules:

Type	Port	Source
HTTP	80	0.0.0.0/0
SSH	22	Admin IP
🖥️ 3. EC2 Access Setup (Passwordless SSH)
🔹 Create SSH Key on aws-client
mkdir -p /root/.ssh
chmod 700 /root/.ssh

[ -f /root/.ssh/id_rsa ] || ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa -N ""
🔹 Copy Public Key to EC2
ssh-copy-id -i /root/.ssh/id_rsa.pub ec2-user@<EC2_PUBLIC_IP>

OR manual:

cat /root/.ssh/id_rsa.pub

Paste into EC2:

mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "<PUBLIC_KEY>" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
📂 4. Deploy Application File (index.php)
Copy file from aws-client to EC2
scp /root/index.php ec2-user@<EC2_PUBLIC_IP>:/tmp/

Move to web directory:

sudo mv /tmp/index.php /var/www/html/index.php
sudo chmod 644 /var/www/html/index.php
🌐 5. Install & Configure Web Server (EC2)
sudo yum install apache2.service -y
sudo systemctl enable apache2.service
sudo systemctl start apache2.service
🔌 6. Configure Database Connection (PHP)

Edit file:

sudo vi /var/www/html/index.php
Update DB credentials:
<?php
$host = "nautilus-rds.xxxxxx.ap-south-1.rds.amazonaws.com";
$username = "nautilus_admin";
$password = "YOUR_PASSWORD";
$dbname = "nautilus_db";

$conn = new mysqli($host, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

echo "Connected successfully";
?>
🧪 7. Test Database Connectivity
Install MySQL client on EC2
sudo yum install mysql -y
Test connection
mysql -h <RDS_ENDPOINT> -u nautilus_admin -p
✅ 8. Validation

Open in browser:

http://<EC2_PUBLIC_IP>/index.php
Expected Output:
Connected successfully
⚠️ Troubleshooting
Issue	Solution
DB connection failed	Check SG rules (3306 access)
Page not loading	Verify httpd service
Permission denied SSH	Check authorized_keys
RDS unreachable	Ensure same VPC
📌 Summary

✔ Private MySQL RDS created
✔ EC2 ↔ RDS secured via Security Group
✔ Passwordless SSH configured
✔ PHP app deployed on Apache
✔ Successful DB connection verified

📎 Notes
Keep RDS private (no public access)
Never expose DB credentials in production code
Use IAM roles & secrets manager for production upgrades