output "ecr_repository_uri" { value = aws_ecr_repository.application.repository_url }
output "image_publisher_role_arn" { value = aws_iam_role.image_publisher.arn }
output "evidence_bucket" { value = aws_s3_bucket.evidence.id }
output "evidence_kms_key_arn" { value = aws_kms_key.evidence.arn }
output "log_group" { value = aws_cloudwatch_log_group.rehearsal.name }
