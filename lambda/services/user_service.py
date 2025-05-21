from datetime import datetime
from models.user import validate_user
from utils.dynamodb import table
import uuid

def create_user(data):
    is_valid, error = validate_user(data)
    if not is_valid:
        return {"statusCode": 400, "body": {"error": error}}

    user_id = str(uuid.uuid4())
    item = {
        "PK": f"USER#{user_id}",
        "SK": f"PROFILE#{user_id}",
        "email": data["email"],
        "name": data["name"],
        "created_at": datetime.utcnow().isoformat()
    }
    
    table.put_item(Item=item)
    return {"statusCode": 200, "body": {"message": "User created", "user_id": user_id}}

def get_user(user_id):
    response = table.get_item(
        Key={
            "PK": f"USER#{user_id}",
            "SK": f"PROFILE#{user_id}"
        }
    )
    return {"statusCode": 200, "body": response.get("Item", {})}
