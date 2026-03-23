variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "lambda_name" {
  description = "lambda_test_terraform"
  type        = string
  default     = "lambda_collector"
}

variable "lambda_runtime" {
  description = "Lambda runtime"
  type        = string
  default     = "python3.9"
}

variable "lambda_handler" {
  description = "Lambda handler"
  type        = string
  default     = "app.lambda_handler"
}

variable "youtube_api_key" {
  description = "API Key do YouTube"
  type        = string
  sensitive   = true
}