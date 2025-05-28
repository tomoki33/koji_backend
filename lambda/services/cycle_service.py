from datetime import datetime
from utils.dynamodb import table
import json

def create_cycle_log(user_id, cycle_id, data):
    timestamp = datetime.utcnow().isoformat()
    item = {
        "PK": f"USER#{user_id}",
        "SK": f"CYCLE#{cycle_id}#{timestamp}",
        "date": data["date"],
        "time": data["time"],
        "kojiType": data["kojiType"],
        "riceType":data["riceType"],
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
        },
        ScanIndexForward=True  # 昇順で取得
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
    response = table.query(
        KeyConditionExpression="PK = :pk",
        ExpressionAttributeValues={
            ":pk": f"USER#{user_id}"
        },
        Limit=1,
        ScanIndexForward=False
    )
    
    items = response.get("Items", [])
    if items:
        return {
            "statusCode": 200,
            "body": json.dumps(items[0])
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'No cycle logs found'})
        }

def update_cycle_log(user_id, cycle_id, data):
    # まず、該当するアイテムを取得
    response = table.query(
        KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
        ExpressionAttributeValues={
            ":pk": f"USER#{user_id}",
            ":sk": f"CYCLE#{cycle_id}"
        }
    )
    
    items = response.get("Items", [])
    
    # dateとtimeが一致するアイテムを探す
    item_to_update = None
    for item in items:
        if item['date'] == data['date'] and item['time'] == data['time']:
            item_to_update = item
            break
    
    if not item_to_update:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Cycle log not found for the given date and time'})
        }
    
    # 更新するデータを設定
    update_expression = "SET #date = :date, #time = :time, #kojiType = :kojiType, #riceType = :riceType, #roomTemperature = :roomTemperature, #humidity = :humidity, #productTemperature = :productTemperature, #comment = :comment"
    expression_attribute_names = {
        "#date": "date",
        "#time": "time",
        "#kojiType": "kojiType",
        "#riceType": "riceType",
        "#roomTemperature": "roomTemperature",
        "#humidity": "humidity",
        "#productTemperature": "productTemperature",
        "#comment": "comment"
    }
    expression_attribute_values = {
        ":date": data["date"],
        ":time": data["time"],
        ":kojiType": data["kojiType"],
        ":riceType": data["riceType"],
        ":roomTemperature": data["roomTemperature"],
        ":humidity": data["humidity"],
        ":productTemperature": data["productTemperature"],
        ":comment": data["comment"]
    }
    
    # DynamoDBのアイテムを更新
    table.update_item(
        Key={
            "PK": item_to_update["PK"],
            "SK": item_to_update["SK"]
        },
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values
    )
    
    return {
        "statusCode": 200,
        "body": {
            "message": "Cycle log updated successfully"
        }
    }

def get_cycle_log(user_id, cycle_id, date, time):
    response = table.query(
        KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
        ExpressionAttributeValues={
            ":pk": f"USER#{user_id}",
            ":sk": f"CYCLE#{cycle_id}"
        }
    )
    
    items = response.get("Items", [])
    
    # dateとtimeが一致するアイテムを探す
    for item in items:
        if item['date'] == date and item['time'] == time:
            return {
                'statusCode': 200,
                'body': json.dumps(item)
            }
    
    return {
        'statusCode': 404,
        'body': json.dumps({'error': 'Cycle log not found for the given date and time'})
    }
