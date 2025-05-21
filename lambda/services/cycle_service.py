from datetime import datetime
import uuid
from models.cycle import validate_cycle
from utils.dynamodb import table

def create_cycle(user_id, data):
    is_valid, error = validate_cycle(data)
    if not is_valid:
        return {"statusCode": 400, "body": {"error": error}}

    cycle_id = data["start_date"]  # start_dateをcycle_idとして使用
    item = {
        "PK": f"USER#{user_id}",
        "SK": f"CYCLE#{cycle_id}",  # SKにcycle_idを使用
        "end_date": data["end_date"],
        "status": data["status"],
        "notes": data.get("notes", ""),
        "created_at": datetime.utcnow().isoformat()
    }
    
    table.put_item(Item=item)
    return {
        "statusCode": 200, 
        "body": {
            "message": "Cycle created", 
            "cycle_id": cycle_id
        }
    }

def get_user_cycles(user_id):
    response = table.query(
        KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
        ExpressionAttributeValues={
            ":pk": f"USER#{user_id}",
            ":sk": "CYCLE#"
        }
    )
    return {"statusCode": 200, "body": response.get("Items", [])}

def get_cycle(cycle_id):
    response = table.query(
        KeyConditionExpression="SK = :sk",
        ExpressionAttributeValues={
            ":sk": f"CYCLE#{cycle_id}"
        }
    )
    return {"statusCode": 200, "body": response.get("Items", [])}

def update_cycle(cycle_id, data):
    update_expression = "SET "
    expression_values = {}
    expression_names = {}
    
    # 更新可能なフィールド
    updatable_fields = ["status", "notes", "end_date"]
    
    for field in updatable_fields:
        if field in data:
            update_expression += f"#{field} = :{field}, "
            expression_values[f":{field}"] = data[field]
            expression_names[f"#{field}"] = field
    
    if not expression_values:
        return {"statusCode": 400, "body": {"error": "No valid fields to update"}}
    
    update_expression = update_expression.rstrip(", ")
    
    try:
        response = table.update_item(
            Key={
                "SK": f"CYCLE#{cycle_id}"
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ExpressionAttributeNames=expression_names,
            ReturnValues="ALL_NEW"
        )
        return {"statusCode": 200, "body": response.get("Attributes", {})}
    except Exception as e:
        return {"statusCode": 500, "body": {"error": str(e)}}
