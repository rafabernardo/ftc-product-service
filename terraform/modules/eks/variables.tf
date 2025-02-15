variable "eks_name" {
  type = string
}

variable "node_group_name" {
  type = string
}

variable "node_instance_type" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}

variable "security_group_id" {
  type = string
}

variable "access_config" {
  type = string
}

variable "region" {
  type = string
}

variable "account_id" {
  type = string
}

variable "policy_arn" {
  type = string
}

variable "role_arn" {
  type = string
}
