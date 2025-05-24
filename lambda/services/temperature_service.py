from datetime import datetime
from utils.dynamodb import table
import json
import uuid

def create_cycle_log(user_id, cycle_id, data):
    timestamp = datetime.utcnow().isoformat()
    unique_id = str(uuid.uuid4())  # ユニークなIDを生成
    item = {
        "PK": f"USER#{user_id}",
        "SK": f"CYCLE#{cycle_id}#{unique_id}",  # ユニークなIDをSKに追加
        "time": data["time"],
        "roomTemperature": data["roomTemperature"],
        "humidity": data["humidity"],
        "productTemperature": data["productTemperature"],
        "comment": data["comment"],
        "created_at": timestamp
    }
    
    table.put_item(Item=item)
    return {
        "statusCode": 200, 
        "body": {
            "message": "Temperature log created",
            "timestamp": timestamp
        }
    }

def get_cycle_logs(user_id, cycle_id):
    response = table.query(
        KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
        ExpressionAttributeValues={
            ":pk": f"USER#{user_id}",
            ":sk": f"CYCLE#{cycle_id}#"
        }
    )
    items = response.get("Items", [])
    if items:
        return {
            "statusCode": 200,
            "body": json.dumps(items)
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Cycle not found'})
        }

def get_latest_cycle_log(user_id):
    # DynamoDBから最新のサイクルログを取得するロジック
    response = table.query(
        KeyConditionExpression="PK = :pk",
        ExpressionAttributeValues={
            ":pk": f"USER#{user_id}"
        },
        Limit=1,  # 最新の1つを取得
        ScanIndexForward=False  # 降順で取得
    )
    
    items = response.get("Items", [])
    if items:
        return {
            "statusCode": 200,
            "body": json.dumps(items[0])  # 最新のサイクルログを返す
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'No cycle logs found'})
        }
