terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }

  backend "s3" {
    bucket = "lambda-collector-tfstate"
    key    = "lambda/terraform.tfstate"
    region = "us-east-1"
  }
}