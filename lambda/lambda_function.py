import boto3
from zipfile import ZipFile

import os
import json
import uuid
myuuid = str(uuid.uuid4()).replace('-','')
glue_job_name='csv-to-parquet-job'
def lambda_handler(event, context):
    # TODO implement
    for record in event['Records']:
        file_name_with_directory = record['s3']['object']['key']
        file_name = record['s3']['object']['key'].split('/')[0]
        bucketName=record['s3']['bucket']['name']
        print("File Name : ",file_name)
        print("File Name with directory: ",file_name_with_directory)
        print("Bucket Name : ",bucketName)
        local_file_full_name='/tmp/{}'.format(file_name)
        s3 = boto3.client('s3')
        s3.download_file(bucketName, file_name_with_directory, local_file_full_name)
        print("File downloaded successfully")
        
        with ZipFile(local_file_full_name, 'r') as f:
            #extract in current directory
            f.extractall('/tmp/unzip{}'.format(myuuid))
        file_names=''
        for filename in os.listdir('/tmp/unzip{}'.format(myuuid)):
            f = os.path.join('/tmp/unzip{}'.format(myuuid), filename)
            print("File Name : ",f)
            s3.upload_file(f, bucketName, 'curated/{}'.format(filename))
            os.remove(f)
            file_names=file_names+','+'s3://{}/curated/{}'.format(bucketName,filename)
        print("Files after unzip :", file_names)
        glue=boto3.client('glue');
        response = glue.start_job_run(JobName = glue_job_name, Arguments={"--VAL1":file_names[1:]})
        print("Glue Job trigger response : ",response)
        return {
            'statusCode': 200,
            'body': json.dumps('Lambda test..')
        }