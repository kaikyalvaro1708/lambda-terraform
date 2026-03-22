output "lambda_name" {
  description = "Lambda name"
  value       = aws_lambda_function.lambda.function_name
}

output "lambda_arn" {
  description = "Lambda ARN"
  value       = aws_lambda_function.lambda.arn
}

output "lambda_invoke_arn" {
  description = "Invoke ARN"
  value       = aws_lambda_function.lambda.invoke_arn
}