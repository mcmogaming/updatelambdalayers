import json
import boto3


def lambda_handler(event, context):
    data = json.loads(event['body'])

    http = event['requestContext']['http']['path']
    http_method = http['method']
    http_path = http['path']

    if http_path == "UploadNewLayerVersion":
        layer = data['layer']
        zip_location = data['zip_location']

        layer_response = boto3.client('lambda').publish_layer_version(
            LayerName=layer['name'],
            Description=layer['description'],
            Content={
                'S3Bucket': zip_location['S3Bucket'],
                'S3Key': zip_location['S3Key'],
            },
            CompatibleRuntimes=layer['compatible_runtimes'],
            LicenseInfo=layer['license_info'],
            CompatibleArchitectures=layer['compatible_architectures']
        )
        return {
            'statusCode': 200,
            'body': {
                'message': "Published Layer Version",
                'layer': layer_response
            }
        }
    elif http_path == "UpdateFunctionToLatestVersion":
        function = data['function']
        layer = data['layer']

        # Get current function configuration
        function_configuration = boto3.client(
            'lambda').get_function_configuration(FunctionName=function['name'])

        # Get a list of all versions for that layer

        layer_versions_paginator = boto3.client(
            'lambda').get_paginator('list_layer_versions')
        layer_versions = layer_versions_paginator.paginate(
            CompatibleRuntime='nodejs' | 'nodejs4.3' | 'nodejs6.10' | 'nodejs8.10' | 'nodejs10.x' | 'nodejs12.x' | 'nodejs14.x' | 'nodejs16.x' | 'java8' | 'java8.al2' | 'java11' | 'python2.7' | 'python3.6' | 'python3.7' | 'python3.8' | 'python3.9' | 'dotnetcore1.0' | 'dotnetcore2.0' | 'dotnetcore2.1' | 'dotnetcore3.1' | 'dotnet6' | 'nodejs4.3-edge' | 'go1.x' | 'ruby2.5' | 'ruby2.7' | 'provided' | 'provided.al2' | 'nodejs18.x' | 'python3.10' | 'java17',
            LayerName='string',
            CompatibleArchitecture='x86_64' | 'arm64',
            PaginationConfig={
                'MaxItems': 10,
                'PageSize': 1,
                'StartingToken': 'string'
            }
        )

        # Get the maximum version value
        maximum_version = 0
        maximum_version_arn = ""
        for layer_ in layer_versions['LayerVersions']:
            if layer_['Version'] > maximum_version:
                maximum_version = layer_['version']
                maximum_version_arn = layer_['LayerVersionArn']

        # Remove the layer from the layer list in current function config

        layers_config_arns = [layer_config['Arn']
                              for layer_config in function_configuration['Layers']]

        found = False
        LAYER_NAME_INDEX = -2
        LAYER_VERSION_INDEX = -1
        for current_layer_arn_index in range(0, len(layers_config_arns)):
            arn = layers_config_arns[current_layer_arn_index]
            arn_segments = arn.split(':')
            if arn_segments[LAYER_NAME_INDEX] == layer['name']:
                found = True
                # Set the arn to the new version
                arn_segments[LAYER_VERSION_INDEX] = str(maximum_version_arn)
                # Remove old arn and insert new arn
                layers_config_arns.pop(current_layer_arn_index)
                layers_config_arns.push(arn_segments.join(':'))

        # Error handling if layer was not added to function before function call
        if not found:
            return {
                'statusCode': 400,
                'body': {
                    'message': "The layer not found in functions layer list"
                }
            }

        # Update the function configuration
        response_object = boto3.client('lambda').update_function_configuration(
            FunctionName=function['name'],
            Layers=layers_config_arns
        )

        return {
            'statusCode': 200,
            'body': {
                'message': "Successfully updated function to latest layer version",
                'response': response_object
            }
        }
    elif http_path == "UpdateFunctionToSpecificVersion":
        function = data['function']
        layer = data['layer']

        # Get current function configuration
        function_configuration = boto3.client(
            'lambda').get_function_configuration(FunctionName=function['name'])

        # Remove the layer from the layer list in current function config

        layers_config_arns = [layer_config['Arn']
                              for layer_config in function_configuration['Layers']]

        found = False
        LAYER_NAME_INDEX = -2
        LAYER_VERSION_INDEX = -1
        for current_layer_arn_index in range(0, len(layers_config_arns)):
            arn = layers_config_arns[current_layer_arn_index]
            arn_segments = arn.split(':')
            if arn_segments[LAYER_NAME_INDEX] == layer['name']:
                found = True
                # Set the arn to the new version
                arn_segments[LAYER_VERSION_INDEX] = str(layer['version'])
                # Remove old arn and insert new arn
                layers_config_arns.pop(current_layer_arn_index)
                layers_config_arns.push(arn_segments.join(':'))

        # Error handling if layer was not added to function before function call
        if not found:
            return {
                'statusCode': 400,
                'body': {
                    'message': "The layer not found in functions layer list"
                }
            }

        # Update the function configuration
        response_object = boto3.client('lambda').update_function_configuration(
            FunctionName=function['name'],
            Layers=layers_config_arns
        )

        return {
            'statusCode': 200,
            'body': {
                'message': "Successfully updated function to latest layer version",
                'response': response_object
            }
        }
    else:
        return {
            'satusCode': 404,
            'body': {
                'message': "Please use a valid endpoint"
            }
        }
