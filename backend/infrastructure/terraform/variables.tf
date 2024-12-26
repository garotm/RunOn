variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud Region"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "development"
}

variable "function_memory" {
  description = "Memory allocation for Cloud Functions"
  type        = number
  default     = 256
} 