# ユーザー関連のルート
resource "aws_apigatewayv2_route" "create_user" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "POST /users"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
  
  # 認証設定を追加
  authorization_type = "JWT"
  authorizer_id     = aws_apigatewayv2_authorizer.cognito.id
}

resource "aws_apigatewayv2_route" "get_user" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "GET /users/{user_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
  
  # 認証設定を追加
  authorization_type = "JWT"
  authorizer_id     = aws_apigatewayv2_authorizer.cognito.id
}

# サイクル関連のルート
resource "aws_apigatewayv2_route" "get_cycle" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "GET /cycles/{cycle_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
  
  # 認証設定を追加
  authorization_type = "JWT"
  authorizer_id     = aws_apigatewayv2_authorizer.cognito.id
}

resource "aws_apigatewayv2_route" "update_cycle" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "PUT /cycles/{cycle_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
  
  # 認証設定を追加
  authorization_type = "JWT"
  authorizer_id     = aws_apigatewayv2_authorizer.cognito.id
}

# 温度記録関連のルート
resource "aws_apigatewayv2_route" "create_temperature_log" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "POST /cycles/{cycle_id}/logs"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
  
  # 認証設定を追加
  authorization_type = "JWT"
  authorizer_id     = aws_apigatewayv2_authorizer.cognito.id
}

resource "aws_apigatewayv2_route" "get_cycle_logs" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "GET /cycles/{cycle_id}/logs"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
  
  # 認証設定を追加
  authorization_type = "JWT"
  authorizer_id     = aws_apigatewayv2_authorizer.cognito.id
}

resource "aws_apigatewayv2_route" "get_temperature_stats" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "GET /cycles/{cycle_id}/stats"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
  
  # 認証設定を追加
  authorization_type = "JWT"
  authorizer_id     = aws_apigatewayv2_authorizer.cognito.id
}

resource "aws_apigatewayv2_route" "get_latest_temperature" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "GET /cycles/{cycle_id}/latest"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
  
  # 認証設定を追加
  authorization_type = "JWT"
  authorizer_id     = aws_apigatewayv2_authorizer.cognito.id
}
