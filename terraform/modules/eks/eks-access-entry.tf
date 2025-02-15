resource "aws_eks_access_entry" "access-entry" {
  cluster_name      = aws_eks_cluster.eks-fiap-tech.name
  principal_arn     = "arn:aws:iam::${var.account_id}:role/voclabs"
  kubernetes_groups = ["fiap"]
  type              = "STANDARD"
}
