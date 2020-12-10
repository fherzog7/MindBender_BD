import boto3
import pydoop.hdfs as hdfs
from os import path
from botocore.exceptions import NoCredentialsError

def upload_to_s3(s3, hdfs_path, bucket, KEY):
    try:
        file = hdfs.open(hdfs_path)
        s3.Bucket(bucket).put_object(Key=KEY, Body=file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def readFromS3(s3, bucket, KEY):
    try:
        obj = s3.Object(bucket, KEY)
        body = obj.get()['Body'].read()
        print("Read Successful")
        return(body)
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def downloadFile(s3, bucket, KEY):
    try:
        print(path.splitext(file_name))
        obj = s3.Bucket(bucket).download_file(KEY, KEY)
        return obj
        print("Download Successful")
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def makeDirectory(s3, bucket, dirName):
    s3.put_object(Bucket=bucket, Key=(dirName+'/'))

def upload(s3, bucket, filename):
    s3.upload_file(filename,
        bucket, 'teset/{}'.format(filename))

with open("aws_keys.txt") as lines:
    aws_conf = [line.rstrip() for line in lines]

#BUCKET_NAME = aws_conf[0]
#ACCESS_KEY = aws_keys[1]
#AWS_SECRET = aws_keys[2]

BUCKET_NAME = "bucket-eit-rick001"

##################
#USING .AWS CONFIG FOR ACCESS KEYS
##################

#KEY1 = "USC90NIC141D121001.jpg"
#KEY2 = "test.csv"
#file_path = "hdfs://hadoop-master:9000/mockdata/MOCK_DATA.csv"
fname = "cheatsheet"
client = boto3.client("s3", region_name='us-west-2')
upload(client, BUCKET_NAME, fname)







