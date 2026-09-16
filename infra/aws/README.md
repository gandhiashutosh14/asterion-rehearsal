# AWS rehearsal foundation — source only

This Terraform module creates an ECR repository, private encrypted S3 evidence bucket, KMS key, log group, and narrowly scoped GitHub OIDC image-publisher role. It does **not** create an ECS service, application user identity, queue, database, model deployment, or private networking. The application currently exports files locally and does not automatically use this bucket.

**Verification status:** source reviewed, not initialized, formatted, validated or applied with Terraform in the packaging environment. Do not interpret the architecture diagram as implemented IaC coverage.

## Operator prerequisites

Use a disposable account or approved sandbox, billing controls, an existing GitHub OIDC provider, an exact repository name, and a protected GitHub environment named `rehearsal`. Set review and deployment-branch restrictions on that environment; an IAM subject condition does not configure those GitHub controls for you. Use remote encrypted Terraform state with locking for team use; no backend is hard-coded here. The supplied AWS partition validation is for commercial AWS, not GovCloud or China.

After a qualified review, run `terraform fmt -check`, `terraform init`, `terraform validate`, and inspect a saved plan. No apply command is automatically executed by CI. Applying will create resources that can incur charges. ECR tags are immutable, so re-publishing the same commit tag is intentionally not an overwrite operation.

## GitHub image publication

The manual workflow reads repository/environment variables `AWS_REGION`, `AWS_IMAGE_ROLE_ARN`, and `ECR_REPOSITORY_URI`. Populate these from reviewed outputs. Its role may push an image to one repository; it has no rights to deploy workloads or read evidence. This separates image publication from release authority.

## Data and cleanup

Versioning is enabled, but Object Lock, legal retention, object signing, per-tenant IAM and evidence uploads are not configured. Encryption at rest is not tenant isolation. A nonempty evidence bucket must be intentionally emptied before deletion; the KMS key has a 30-day deletion waiting period. Preserve required evidence before any cleanup. The log group uses a short 14-day synthetic-demo retention, not a customer retention commitment.

See [cloud architecture](../../docs/CLOUD_ARCHITECTURE.md) for the service target and its unimplemented prerequisites.
