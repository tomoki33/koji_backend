# 温度記録関連のルート
resource "aws_apigatewayv2_route" "create_cycle_log" {
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

resource "aws_apigatewayv2_route" "get_latest_cycle_log" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "GET /cycles/latest-log"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
  
  # 認証設定を追加
  authorization_type = "JWT"
  authorizer_id     = aws_apigatewayv2_authorizer.cognito.id
}

resource "aws_apigatewayv2_route" "update_cycle_log" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "POST /cycles/update/{cycle_id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
  
  # 認証設定を追加
  authorization_type = "JWT"
  authorizer_id     = aws_apigatewayv2_authorizer.cognito.id
}

resource "aws_apigatewayv2_route" "get_cycle_log" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "GET /cycles/{cycle_id}/{date}/{time}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
  
  # 認証設定を追加
  authorization_type = "JWT"
  authorizer_id     = aws_apigatewayv2_authorizer.cognito.id
}
