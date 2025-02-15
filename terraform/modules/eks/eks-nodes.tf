resource "aws_eks_node_group" "eks-fiap-tech-node" {
  cluster_name    = aws_eks_cluster.eks-fiap-tech.name
  node_group_name = var.node_group_name
  node_role_arn   = var.role_arn
  subnet_ids      = var.subnet_ids
  disk_size       = 20
  instance_types = [
    var.node_instance_type
  ]


  scaling_config {
    desired_size = 1
    min_size     = 1
    max_size     = 2
  }

  depends_on = [aws_eks_cluster.eks-fiap-tech]
}
