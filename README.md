# aws-practice-lab — AWS runbooks & hands-on labs

Welcome — this repository is a curated collection of practical AWS runbooks and labs for DevOps engineers and learners. Each guide is a self-contained, step-by-step procedure (console + CLI + verification + cleanup) for common AWS tasks: EC2, VPC, S3, ECR/ECS (Fargate), EKS, RDS, KMS, Lambda, SNS/SQS, and troubleshooting SOPs.

Prerequisites
- AWS CLI configured (or use an appropriate IAM role)
- Docker (for ECR/ECS labs)
- kubectl (for EKS labs)
- An AWS account with permissions matching the target guide (most guides call out required IAM permissions)

Structure
- aws-tasks/ — individual labs and runbooks (one Markdown file per task). The repository contains guides, example CloudFormation, and small code snippets (e.g., inline Lambda Python).

Quick start — recommended first labs
1. create_public_vpc_and_ec2_instance.md — Basic VPC + EC2 instance provisioning and verification (good first lab).
2. create_ec2_instance_with_nginx_using_user_data.md — EC2 user-data provisioning of nginx (automated web server setup).
3. aws_s3_static_website_hosting.md — Host a static site on S3, public bucket & website endpoint.
4. Deploying_Application_on_ECS_using_Fargate.md — Build/push Docker image to ECR and deploy to ECS Fargate.
5. eks_cluster_private_setup.md — Create a private-only EKS control plane and validate kubectl connectivity.
6. aws_kms_encrypt_decrypt_sensitive_file.md — Hands-on KMS symmetric key usage: encrypt/decrypt files.
7. devops-priority-stack.md / devops-priority-stack.py — CloudFormation SNS/SQS/Lambda priority queuing system (good for serverless + messaging learning).

Full index (aws-tasks/) — file → one-line summary
- AWS Secure Log Aggregation Setup.md — Guide for creating a secure centralized log aggregation pipeline on AWS.
- AWS_ASG_ALB_Setup.md — Configure Auto Scaling Group behind an Application Load Balancer.
- Configure Application Load Balancer.md — ALB configuration and listener/target group setup.
- Create AMI from Existing EC2 Instance.md — Steps to create and manage AMIs from a running EC2.
- Create EC2 Instance with Passwordless SSH.md — Provision EC2 and set up SSH key-based access.
- Create IAM Policy.md — How to create and attach custom IAM policies for common tasks.
- Create Private S3 Bucket and Migrate Data.md — Create private S3 buckets and migrate/transfer data securely.
- Delete EC2 Instance.md — Safe removal of EC2 instances with cleanup checklist.
- Deploying_Application_on_ECS_using_Fargate.md — ECR image build/push + ECS Fargate task & service creation.
- EBS_Volume_Expansion_SOP.md — Standard operating procedure to expand EBS volumes and grow filesystems.
- Managing_EC2_Access_with_S3_Role-based_Permissions.md — Use IAM roles to grant EC2 instances S3 access securely.
- Private RDS Setup & EC2 Integration.md — Create private RDS instances and integrate with EC2 hosts.
- S3_lambda_copy_automation.md — Lambda-driven automation to copy/move objects between S3 buckets.
- attach_eni_to_ec2_instance.md — Attach/assign additional ENIs to running EC2 instances.
- aws-ec2-alb-nginx-setup.md — Deploy nginx on EC2 and place it behind an ALB.
- aws_RDS_setup_EC2_Integration.md — RDS provisioning and network connectivity to EC2 (similar to Private RDS guide).
- aws_ec2_nginx_vpc_troubleshooting.md — Troubleshooting checklist for EC2/nginx connectivity (IGW, routes, SGs, NACLs).
- aws_kms_encrypt_decrypt_sensitive_file.md — KMS symmetric key examples for encrypting/decrypting files (CLI examples provided).
- aws_lambda_cli_health_check.md — Create Lambda-based health checks and run them via CLI.
- aws_lambda_devops_lambda.md — Examples of Lambda for DevOps automation tasks.
- aws_nat_gateway_setup_for_private_ec_2_internet_access.md — Configure NAT gateway for private subnets to access the Internet.
- aws_rds_snapshot_restore.md — Take RDS snapshots and restore procedures for backups / recovery testing.
- aws_s3_static_website_hosting.md — S3 website hosting: bucket policy, public access block, and website endpoint.
- create_ec2_instance_with_nginx_using_user_data.md — Example user-data script to bootstrap nginx on EC2.
- create_public_vpc_and_ec2_instance.md — Simple VPC + public subnet + EC2 provisioning guide.
- devops-priority-stack.md — Runbook for deploying SNS → SQS priority queues with Lambda processing.
- devops-priority-stack.py — CloudFormation template (YAML) with inline Lambda code for the priority queue stack.
- dynamo_db_to_do_app_console_cli_json_guide.md — Build a DynamoDB-backed TODO app (console + CLI + JSON examples).
- ecr_docker_image_push.md — Authenticate Docker to ECR and push images (ECR login & push examples).
- eks_cluster_private_setup.md — Create a private-only Amazon EKS cluster (console + aws CLI examples).
- enable_stop_protection_for_ec2_instance.md — How to enable termination/stop protection to prevent accidental shutdowns.
- launch_ec2_instance_and_create_cloudwatch_alarm.md — Launch EC2 and configure CloudWatch alarm(s) for instance metrics.
- nat_instance_setup_private_ec2_s3_access.md — NAT instance pattern for private EC2 to access S3 (older alternative to NAT gateway).
- nautilus-lambda-app.md — Example Lambda application (project layout and deployment notes).
- private_rds_create.md — Create RDS instances in private subnets and associated connectivity steps.

Security notes
- Many guides demonstrate enabling public access (S3) or opening HTTP for ease of testing. Review each guide’s “Prerequisites” and “Important Notes” sections and adapt policies/security groups for production.
- Replace example resource names, account IDs, and keys with your own values before running commands.

How to use this repo
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-org-or-username>/aws-practice-lab.git
   cd aws-practice-lab/aws-tasks
   ```
2. Pick a guide (start with the recommended list), review the prerequisites and any hard-coded names in the file, then run the CLI commands step-by-step.
3. For CloudFormation templates (devops-priority-stack), copy the template into a .yml and run `aws cloudformation create-stack` (examples are in the markdown).

Contributing
- Add new lab guides to aws-tasks/ as Markdown files and follow the existing structure:
  - Objective → Architecture → Prerequisites → Console steps → CLI steps → Verification → Cleanup → Notes.
- Keep examples reproducible and call out any default/public/insecure settings clearly.
- Open a PR with one lab per file, include sample commands and any artifacts (task definitions, policy JSON, CloudFormation templates).

Want me to commit this README.md for you?
I can create README.md in the repository directly and open a PR (or commit to the default branch) if you grant me the repository name and permission to write. I can also:
- Convert devops-priority-stack.py into a proper devops-priority-stack.yml file,
- Add a short Makefile with targets like `make deploy-priority-stack` and `make cleanup`.

License
- Add your preferred license file (e.g., MIT) at the repository root if you want to make this content shareable.

Contact / Support
- For clarifications or to request a PR that adds the README to the repo, reply with "Create README" and confirm whether to commit to main or open a pull request.
