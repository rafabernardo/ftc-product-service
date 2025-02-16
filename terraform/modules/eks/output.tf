output "cluster_name" {
  value = aws_eks_cluster.eks-fiap-tech.name
}

output "node_group_name" {
  value = aws_eks_node_group.eks-fiap-tech-node.node_group_name
}

output "endpoint" {
  value = aws_eks_cluster.eks-fiap-tech.endpoint
}

output "cluster_certificate_authority" {
  value = aws_eks_cluster.eks-fiap-tech.certificate_authority[0].data
}
