import boto3

dynamodb = boto3.resource('dynamodb')

TABLE_NAME = 'koji_data'
table = dynamodb.Table(TABLE_NAME)