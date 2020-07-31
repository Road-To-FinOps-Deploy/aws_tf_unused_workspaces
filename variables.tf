variable "unused_workspaces_cleanup_cron" {
  description = "interval of time to trigger lambda function"
  default     = "cron(0 8 1 * ? *)"
}

variable "function_prefix" {
  default = ""
}


variable "days" {
  default = "28"
}
