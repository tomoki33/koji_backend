#!/bin/bash

# 環境変数の設定
USER_POOL_ID=$(terraform output -raw user_pool_id)
CLIENT_ID=$(terraform output -raw client_id)
API_ENDPOINT=$(terraform output -raw api_endpoint)
USERNAME="test@example.com"
PASSWORD="Test123!"

echo "User Pool ID: $USER_POOL_ID"
echo "Client ID: $CLIENT_ID"
echo "API Endpoint: $API_ENDPOINT"


# 1. テストユーザーの作成
echo "1. テストユーザーを作成"
aws cognito-idp admin-create-user \
    --user-pool-id $USER_POOL_ID \
    --username $USERNAME \
    --temporary-password $PASSWORD \
    --user-attributes Name=email,Value=$USERNAME

# 2. パスワードの永続化
echo "2. パスワードを永続化"
aws cognito-idp admin-set-user-password \
    --user-pool-id $USER_POOL_ID \
    --username $USERNAME \
    --password $PASSWORD \
    --permanent

# 3. ログイン（認証トークンの取得）
echo "3. ログインをテスト"
AUTH_RESULT=$(aws cognito-idp admin-initiate-auth \
    --user-pool-id $USER_POOL_ID \
    --client-id $CLIENT_ID \
    --auth-flow ADMIN_USER_PASSWORD_AUTH \
    --auth-parameters USERNAME=$USERNAME,PASSWORD=$PASSWORD)

# トークンの抽出
ID_TOKEN=$(echo $AUTH_RESULT | jq -r '.AuthenticationResult.IdToken')
ACCESS_TOKEN=$(echo $AUTH_RESULT | jq -r '.AuthenticationResult.AccessToken')

echo "ID Token: $ID_TOKEN"
echo "Access Token: $ACCESS_TOKEN"

# 4. APIリクエストのテスト
curl -X GET $API_ENDPOINT/users/me \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json"
# 5. 無効なトークンでのテスト
echo "5. 無効なトークンでのテスト"
curl -X GET $API_ENDPOINT/users/me \
    -H "Authorization: Bearer invalid_token" \
    -H "Content-Type: application/json"

# # テストユーザーの削除
# echo "テストユーザーを削除"
# aws cognito-idp admin-delete-user \
#     --user-pool-id $USER_POOL_ID \
#     --username $USERNAME