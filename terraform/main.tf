# ZIP AUTOMÁTICO
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda"
  output_path = "${path.module}/lambda.zip"
}

# IAM ROLE
resource "aws_iam_role" "lambda_role" {
  name = "${var.lambda_name}_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# POLICY BÁSICA (logs)
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# LAMBDA
resource "aws_lambda_function" "lambda" {
  function_name = var.lambda_name

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  handler = var.lambda_handler
  runtime = var.lambda_runtime

  role = aws_iam_role.lambda_role.arn

  timeout = 15

#   environment {
#     variables = {
#       YOUTUBE_API_KEY = var.youtube_api_key
#     }
#   }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_basic
  ]
}