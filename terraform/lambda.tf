# Lambda Layer
resource "aws_lambda_layer_version" "dependencies" {
  filename         = "./lambda-layer.zip"
  layer_name       = "koji-dependencies"
  description      = "Dependencies for Koji Lambda functions"
  compatible_runtimes = ["python3.11"]
}

# Lambda関数
resource "aws_lambda_function" "koji_api" {
  filename         = "../handler.zip"
  function_name    = "kojiApiHandler"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.11"
  source_code_hash = filebase64sha256("../handler.zip")
  
  # レイヤーを追加
  layers = [aws_lambda_layer_version.dependencies.arn]
}
