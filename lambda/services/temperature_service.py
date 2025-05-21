from datetime import datetime
from models.temperature import validate_temperature_log
from utils.dynamodb import table

def create_temperature_log(cycle_id, data):
    is_valid, error = validate_temperature_log(data)
    if not is_valid:
        return {"statusCode": 400, "body": {"error": error}}

    timestamp = datetime.utcnow().isoformat()
    item = {
        "PK": f"USER#{user_id}",
        "SK": f"CYCLE#{cycle_id}", 
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "time": data["time"],
        "notes": data["notes"],
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

def get_cycle_logs(cycle_id):
    response = table.query(
        KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
        ExpressionAttributeValues={
            ":pk": f"CYCLE#{cycle_id}",
            ":sk": "LOG#"
        }
    )
    return {"statusCode": 200, "body": response.get("Items", [])}

def get_temperature_stats(cycle_id):
    response = table.query(
        KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
        ExpressionAttributeValues={
            ":pk": f"CYCLE#{cycle_id}",
            ":sk": "LOG#"
        }
    )
    
    logs = response.get("Items", [])
    if not logs:
        return {"statusCode": 200, "body": {"message": "No logs found"}}
    
    # 温度と湿度の統計を計算
    temperatures = [float(log["temperature"]) for log in logs]
    humidities = [float(log["humidity"]) for log in logs]
    
    stats = {
        "temperature": {
            "min": min(temperatures),
            "max": max(temperatures),
            "avg": sum(temperatures) / len(temperatures)
        },
        "humidity": {
            "min": min(humidities),
            "max": max(humidities),
            "avg": sum(humidities) / len(humidities)
        },
        "total_logs": len(logs)
    }
    
    return {"statusCode": 200, "body": stats}

def get_latest_temperature(cycle_id):
    response = table.query(
        KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
        ExpressionAttributeValues={
            ":pk": f"CYCLE#{cycle_id}",
            ":sk": "LOG#"
        },
        ScanIndexForward=False,  # 降順で取得
        Limit=1  # 最新の1件のみ
    )
    
    items = response.get("Items", [])
    if not items:
        return {"statusCode": 404, "body": {"message": "No temperature logs found"}}
    
    return {"statusCode": 200, "body": items[0]}
