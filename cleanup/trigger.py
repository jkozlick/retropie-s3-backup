import boto3
import os

keep = 3
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    record = event['Records'][0]['s3']
    bucket = record['bucket']['name']
    key = record['object']['key']
    
    response = s3_client.list_object_versions(
        Bucket=bucket,
        Prefix=key
    )
    
    version_len = len(response['Versions'])

    if version_len > keep:
        sorted_versions = sorted(
            response['Versions'], 
            key = lambda version: version['LastModified'],
            reverse = True
        )

        for a_version in sorted_versions[keep:version_len]:
            s3_client.delete_object(
                Bucket=bucket,
                Key=key,
                VersionId=a_version['VersionId']
            )
        
        earliest = sorted_versions[keep-1]['LastModified']
        delete_markers = response.get('DeleteMarkers') or []

        for delete_marker in delete_markers:
            if delete_marker['LastModified'] <= earliest:
                s3_client.delete_object(
                    Bucket=bucket,
                    Key=key,
                    VersionId=delete_marker['VersionId']
            )

if __name__ == '__main__':
    import json
    with open(os.environ['RP_TEST_EVENT']) as file:
        event = json.loads(file.read())
    lambda_handler(event, 'context')

