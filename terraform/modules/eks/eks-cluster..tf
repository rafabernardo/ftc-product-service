resource "aws_eks_cluster" "eks-fiap-tech" {
  name     = var.eks_name
  role_arn = var.role_arn

  vpc_config {
    endpoint_public_access = "true"
    public_access_cidrs    = ["0.0.0.0/0"]
    subnet_ids             = var.subnet_ids
    security_group_ids     = [var.security_group_id]
  }

  access_config {
    authentication_mode = var.access_config
  }
}

