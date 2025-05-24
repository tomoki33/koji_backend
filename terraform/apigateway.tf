resource "aws_apigatewayv2_api" "http_api" {
  name          = "koji-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = ["*"]  # 全てのオリジンを許可
    allow_methods = ["*"]  # 許可するメソッド
    allow_headers = ["*"]  # 許可するヘッダー
  }
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "$default"
  auto_deploy = true
}

# Lambda関数との統合設定
resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.http_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.koji_api.invoke_arn
}

# Lambda関数の実行権限
resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.koji_api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http_api.execution_arn}/*/*"
}