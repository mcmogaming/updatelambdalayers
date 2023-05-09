import json
import boto3

def lambda_handler(event, context):
    
    # location = event['CodePipeline.job'].data.inputArtifacts[0]

    layerzip = boto3.resource('s3').get_object(Bucket='lambdalayersbuildbucket',Key='messageLibrary.zip')
    
    # boto3.client.publish_layer_version(
    # LayerName='messageLibraryLayer',
    # Description='message library',
    # Content={
    #     'S3Bucket': 'lambdalayersbuildbucket',
    #     'S3Key': 'messageLibrary.zip',
    #     'S3ObjectVersion': 'string',
    #     'ZipFile': b'bytes'
    # },
    # CompatibleRuntimes=[
    #     'nodejs'|'nodejs4.3'|'nodejs6.10'|'nodejs8.10'|'nodejs10.x'|'nodejs12.x'|'nodejs14.x'|'nodejs16.x'|'java8'|'java8.al2'|'java11'|'python2.7'|'python3.6'|'python3.7'|'python3.8'|'python3.9'|'dotnetcore1.0'|'dotnetcore2.0'|'dotnetcore2.1'|'dotnetcore3.1'|'dotnet6'|'nodejs4.3-edge'|'go1.x'|'ruby2.5'|'ruby2.7'|'provided'|'provided.al2'|'nodejs18.x'|'python3.10'|'java17',
    # ],
    # LicenseInfo='string',
    # CompatibleArchitectures=[
    #     'x86_64'|'arm64',
    # ]
    #)
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'layerzip': layerzip
    }
