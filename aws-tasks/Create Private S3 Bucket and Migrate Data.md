# 7. Create Private S3 Bucket and Migrate Data

### Task
Create bucket `xfusion-sync-15888` and migrate data from `xfusion-s3-25260`.

### AWS CLI Commands
```bash
# Create bucket
aws s3api create-bucket \
  --bucket xfusion-sync-15888 \
  --region us-east-1

# Block public access
aws s3api put-public-access-block \
  --bucket xfusion-sync-15888 \
  --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

# Sync data
aws s3 sync s3://xfusion-s3-25260 s3://xfusion-sync-15888

# Verify consistency
aws s3 sync s3://xfusion-s3-25260 s3://xfusion-sync-15888 --dryrun
```

---
## Create S3 Bucket and Migrate Data
1. Open S3 Dashboard.
2. Click Create Bucket.
3. Bucket name: `xfusion-sync-15888`.
4. Keep Block Public Access enabled.
5. Create bucket.
6. Use AWS CLI to sync data:
```bash
aws s3 sync s3://xfusion-s3-25260 s3://xfusion-sync-15888
```
7. Verify using dry-run sync.