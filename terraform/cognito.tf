# Cognito User Pool
resource "aws_cognito_user_pool" "koji_pool" {
  name = "koji-user-pool"

  # パスワードポリシー
  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }

  # ユーザー属性の設定
  schema {
    name                = "email"
    attribute_data_type = "String"
    mutable            = true
    required           = true
  }

  # メールアドレスの自動検証
  auto_verified_attributes = ["email"]
}

# Cognito User Pool Client
resource "aws_cognito_user_pool_client" "koji_client" {
  name         = "koji-client"
  user_pool_id = aws_cognito_user_pool.koji_pool.id

  generate_secret = false
  explicit_auth_flows = [
    "ALLOW_USER_SRP_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_ADMIN_USER_PASSWORD_AUTH"
  ]
}

# 現在のリージョンを取得
data "aws_region" "current" {}

# API Gateway認証設定
resource "aws_apigatewayv2_authorizer" "cognito" {
  api_id           = aws_apigatewayv2_api.http_api.id
  authorizer_type  = "JWT"
  identity_sources = ["$request.header.Authorization"]
  name            = "cognito-authorizer"

  jwt_configuration {
    audience = [aws_cognito_user_pool_client.koji_client.id]
    issuer   = "https://cognito-idp.${data.aws_region.current.name}.amazonaws.com/${aws_cognito_user_pool.koji_pool.id}"
  }
}
