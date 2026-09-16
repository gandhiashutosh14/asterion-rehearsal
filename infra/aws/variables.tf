variable "region" {
  type    = string
  default = "us-east-1"
}
variable "name" {
  type    = string
  default = "asterion-rehearsal"
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,24}$", var.name))
    error_message = "Use 3-25 lowercase alphanumeric or hyphen characters, starting with a letter."
  }
}
variable "github_repository" {
  type        = string
  description = "Exact owner/repository allowed to publish images. No wildcard."
  validation {
    condition     = can(regex("^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", var.github_repository))
    error_message = "Provide one exact owner/repository."
  }
}
variable "github_oidc_provider_arn" {
  type        = string
  description = "Existing account OIDC provider for token.actions.githubusercontent.com."
  validation {
    condition     = can(regex("^arn:aws:iam::[0-9]{12}:oidc-provider/token.actions.githubusercontent.com$", var.github_oidc_provider_arn))
    error_message = "Provide the existing GitHub OIDC provider ARN in the target account."
  }
}
