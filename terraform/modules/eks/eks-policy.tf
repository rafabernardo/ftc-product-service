resource "aws_eks_access_policy_association" "eks-policy" {
  cluster_name  = aws_eks_cluster.eks-fiap-tech.name
  policy_arn    = var.policy_arn
  principal_arn = "arn:aws:iam::${var.account_id}:role/voclabs"

  access_scope {
    type = "cluster"
  }
}
