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

variable "region" {
  default = "eu-west-1"
}

variable "send_email" {
  description = "if you want to recive an email for this report"
  default = true 
  type  = bool
}

variable "sender_email" {
  default = ""
  description = "email address from which the email will come from. this will be verified by ses"
}


variable "reciver_email" {
  default = "example@hotmail.com"
  description = "who will recive this email"
}