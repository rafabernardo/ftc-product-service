variable "regionDefault" {
  default = "us-east-1"
}

variable "eksName" {
  default = "eks-fiap-tech"
}

variable "nodeGroupName" {
  default = "eks-fiap-tech-node"
}

variable "nodeInstanceType" {
  default = "t3a.medium"
}

variable "projectName" {
  default = "fiap-tech-challenge"
}

variable "securityGroupeName" {
  default = "eks-sg"
}

variable "instanceType" {
  default = "t3a.medium"
}

variable "policyArn" {
  default = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
}

variable "accessConfig" {
  default = "API_AND_CONFIG_MAP"
}

variable "vpcCidr" {
  default = "172.31.0.0/16"
}

variable "accountId" {
  type    = string
  default = "911766435517"
}

variable "apiImage" {
  default = "ecr-fiap-image:latest"
}

variable "db_url" {
  type = string
}
