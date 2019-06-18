#!/bin/bash
echo "--------------------------------------------"

echo "Hey there! This script will setup boto3 for intel-data-mgmt-for-rt-models."
echo ""
echo ""

pip install boto3

#~/.aws/credentials
#[default]
#aws_access_key_id = YOUR_KEY
#aws_secret_access_key = YOUR_SECRET
#~/.aws/config
#[default]
#region=us-east-1

cd $HOME
cat "import boto3
s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
  print(bucket.name)" > test.py

python3 test.py

git clone https://github.com/boto/boto3.git
cd boto3
virtualenv venv
<wait>
. venv/bin/activate
pip install -r requirements.txt
pip install -e .

echo ""
echo ""
echo ""
