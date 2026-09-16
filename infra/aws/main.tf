# Foundation only: this module intentionally does not deploy the application.
# Requires an existing GitHub OIDC provider in the AWS account.
terraform {
  required_version = ">= 1.6, < 2.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0, < 7.0"
    }
  }
}
provider "aws" { region = var.region }
data "aws_caller_identity" "current" {}

resource "aws_kms_key" "evidence" {
  description             = "ASTERION synthetic evidence encryption"
  enable_key_rotation     = true
  deletion_window_in_days = 30
  tags                    = local.tags
}
resource "aws_kms_alias" "evidence" {
  name          = "alias/${var.name}-evidence"
  target_key_id = aws_kms_key.evidence.key_id
}
resource "aws_s3_bucket" "evidence" {
  bucket        = "${var.name}-evidence-${data.aws_caller_identity.current.account_id}-${var.region}"
  force_destroy = false
  tags          = local.tags
}
resource "aws_s3_bucket_public_access_block" "evidence" {
  bucket                  = aws_s3_bucket.evidence.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
resource "aws_s3_bucket_ownership_controls" "evidence" {
  bucket = aws_s3_bucket.evidence.id
  rule { object_ownership = "BucketOwnerEnforced" }
}
resource "aws_s3_bucket_versioning" "evidence" {
  bucket = aws_s3_bucket.evidence.id
  versioning_configuration { status = "Enabled" }
}
resource "aws_s3_bucket_server_side_encryption_configuration" "evidence" {
  bucket = aws_s3_bucket.evidence.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.evidence.arn
    }
    bucket_key_enabled = true
  }
}
resource "aws_s3_bucket_policy" "transport" {
  bucket = aws_s3_bucket.evidence.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "DenyInsecureTransport"
      Effect    = "Deny"
      Principal = "*"
      Action    = "s3:*"
      Resource  = [aws_s3_bucket.evidence.arn, "${aws_s3_bucket.evidence.arn}/*"]
      Condition = { Bool = { "aws:SecureTransport" = "false" } }
    }]
  })
}
resource "aws_ecr_repository" "application" {
  name                 = var.name
  image_tag_mutability = "IMMUTABLE"
  image_scanning_configuration { scan_on_push = true }
  encryption_configuration { encryption_type = "AES256" }
  tags = local.tags
}
resource "aws_cloudwatch_log_group" "rehearsal" {
  name              = "/asterion/${var.name}"
  retention_in_days = 14
  tags              = local.tags
}
resource "aws_iam_role" "image_publisher" {
  name = "${var.name}-image-publisher"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Federated = var.github_oidc_provider_arn }
      Action    = "sts:AssumeRoleWithWebIdentity"
      Condition = { StringEquals = {
        "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
        "token.actions.githubusercontent.com:sub" = "repo:${var.github_repository}:environment:rehearsal"
      } }
    }]
  })
  tags = local.tags
}
resource "aws_iam_role_policy" "image_publisher" {
  role = aws_iam_role.image_publisher.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["ecr:GetAuthorizationToken"], Resource = "*" },
      { Effect = "Allow", Action = ["ecr:BatchCheckLayerAvailability", "ecr:InitiateLayerUpload", "ecr:UploadLayerPart", "ecr:CompleteLayerUpload", "ecr:PutImage", "ecr:BatchGetImage"], Resource = aws_ecr_repository.application.arn }
    ]
  })
}
locals {
  tags = { Project = "ASTERION", Environment = "synthetic-rehearsal", ManagedBy = "Terraform" }
}
