import json
import boto3

def lambda_handler(event, context):
    
    # location = event['CodePipeline.job'].data.inputArtifacts[0]

    layerzip = boto3.client('s3').get_object(Bucket='lambdalayersbuildbucket',Key='messageLibrary.zip')
    
    layer = boto3.client('lambda').publish_layer_version(
    LayerName='messageLibraryLayer',
    Description='message library',
    Content=layerzip,
    CompatibleRuntimes=[
        'python3.9'
    ],
    LicenseInfo='string',
    CompatibleArchitectures=[
        'x86_64',
    ]
    )
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'layer': layer
    }
