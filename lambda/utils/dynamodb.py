import boto3
from botocore.exceptions import ClientError

# DynamoDBのリソースを作成
dynamodb = boto3.resource('dynamodb')

# テーブル名を指定
TABLE_NAME = 'koji_data'  # ここに実際のテーブル名を入力してください
table = dynamodb.Table(TABLE_NAME)

def get_item(key):
    """指定したキーでアイテムを取得する関数"""
    try:
        response = table.get_item(Key=key)
        return response.get('Item', None)
    except ClientError as e:
        print(f"Error getting item: {e.response['Error']['Message']}")
        return None

def put_item(item):
    """アイテムをテーブルに追加する関数"""
    try:
        table.put_item(Item=item)
    except ClientError as e:
        print(f"Error putting item: {e.response['Error']['Message']}")

def update_item(key, update_expression, expression_attribute_values):
    """アイテムを更新する関数"""
    try:
        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return response
    except ClientError as e:
        print(f"Error updating item: {e.response['Error']['Message']}")
        return None

def query_items(key_condition_expression, expression_attribute_values):
    """条件に基づいてアイテムをクエリする関数"""
    try:
        response = table.query(
            KeyConditionExpression=key_condition_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return response
    except ClientError as e:
        print(f"Error querying items: {e.response['Error']['Message']}")
        return None