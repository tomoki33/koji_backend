output "user_pool_id" {
  value = aws_cognito_user_pool.koji_pool.id
}

output "client_id" {
  value = aws_cognito_user_pool_client.koji_client.id
}

output "api_endpoint" {
  value = aws_apigatewayv2_api.http_api.api_endpoint
}
