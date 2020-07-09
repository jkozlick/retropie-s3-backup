import boto3
import os

s3_client = boto3.client('s3')
bucket_name = os.environ.get('BUCKET_NAME')

def lambda_handler(event, context):
    
    return event


if __name__ == '__main__':
    import json
    with open('event') as file:
        event = json.loads(file.read())
    print(lambda_handler(event, 'context'))

