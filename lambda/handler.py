import json
import jwt
from services.user_service import create_user, get_user
from services.cycle_service import create_cycle, get_user_cycles
from services.temperature_service import create_temperature_log, get_cycle_logs
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('koji_data')

def get_user_id(event):
    """Cognitoの認証トークンからユーザーIDを取得"""
    try:
        auth_header = event.get('headers', {}).get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        # JWTトークンの検証とユーザーIDの取得
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded['sub']
    except Exception as e:
        print(f"Error getting user ID: {str(e)}")
        return None

def lambda_handler(event, context):
    # 認証チェック
    user_id = get_user_id(event)
    if not user_id:
        return {
            'statusCode': 401,
            'body': json.dumps({'error': 'Unauthorized'})
        }

    http_method = event['httpMethod']
    path = event['path']
    
    try:
        # ユーザー関連のエンドポイント
        if http_method == 'POST' and path == '/users':
            return create_user(json.loads(event['body']))
        elif http_method == 'GET' and path.startswith('/users/'):
            # 自分のユーザー情報のみ取得可能
            requested_user_id = path.split('/')[-1]
            if requested_user_id != user_id:
                return {
                    'statusCode': 403,
                    'body': json.dumps({'error': 'Forbidden'})
                }
            return get_user(user_id)
            
        # サイクル関連のエンドポイント
        elif http_method == 'POST' and path.startswith('/users/'):
            # 自分のサイクルのみ作成可能
            requested_user_id = path.split('/')[2]
            if requested_user_id != user_id:
                return {
                    'statusCode': 403,
                    'body': json.dumps({'error': 'Forbidden'})
                }
            return create_cycle(user_id, json.loads(event['body']))
        elif http_method == 'GET' and path.startswith('/users/'):
            # 自分のサイクルのみ取得可能
            requested_user_id = path.split('/')[2]
            if requested_user_id != user_id:
                return {
                    'statusCode': 403,
                    'body': json.dumps({'error': 'Forbidden'})
                }
            return get_user_cycles(user_id)
            
        # 温度記録関連のエンドポイント
        elif http_method == 'POST' and path.startswith('/cycles/'):
            cycle_id = path.split('/')[2]
            # サイクルが自分のものかチェック
            if not is_cycle_owner(cycle_id, user_id):
                return {
                    'statusCode': 403,
                    'body': json.dumps({'error': 'Forbidden'})
                }
            return create_temperature_log(cycle_id, json.loads(event['body']))
        elif http_method == 'GET' and path.startswith('/cycles/'):
            cycle_id = path.split('/')[2]
            # サイクルが自分のものかチェック
            if not is_cycle_owner(cycle_id, user_id):
                return {
                    'statusCode': 403,
                    'body': json.dumps({'error': 'Forbidden'})
                }
            return get_cycle_logs(cycle_id)
            
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid request'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def is_cycle_owner(cycle_id, user_id):
    """サイクルが指定されたユーザーのものかチェック"""
    try:
        # DynamoDBからサイクル情報を取得
        response = table.get_item(
            Key={
                'PK': f'CYCLE#{cycle_id}',
                'SK': 'METADATA'
            }
        )
        cycle = response.get('Item')
        return cycle and cycle.get('user_id') == user_id
    except Exception as e:
        print(f"Error checking cycle ownership: {str(e)}")
        return False
