import json
import jwt
from services.cycle_service import create_cycle_log, get_cycle_logs, get_latest_cycle_log
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('koji_data')

def get_user_id(event):
    """Cognitoの認証トークンからユーザーIDを取得"""
    try:
        auth_header = event.get('headers', {}).get('authorization', '')
        if not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded['sub']
    except Exception as e:
        print(f"Error getting user ID: {str(e)}")
        return None

def lambda_handler(event,context):
    user_id = get_user_id(event)
    if not user_id:
        return {
            'statusCode': 401,
            'body': json.dumps({'error': 'Unauthorized'})
        }

    http_method = event['httpMethod']
    path = event['path']
    
    try:            
        if http_method == 'POST' and path.startswith('/cycles/'):
            cycle_id = path.split('/')[2]
            response = create_cycle_log(user_id, cycle_id, json.loads(event['body']))
            return {
                'statusCode': response.get('statusCode', 200),
                'body': json.dumps(response.get('body', {}))
            }        
        elif http_method == 'GET' and path == '/cycles/latest-log':
            return get_latest_cycle_log(user_id)
        elif http_method == 'GET' and path.startswith('/cycles/'):
            cycle_id = path.split('/')[2]
            return get_cycle_logs(user_id, cycle_id)            
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid request'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

