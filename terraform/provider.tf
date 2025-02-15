terraform {
  backend "s3" {
    bucket = "fiap-tech-challenge-terraform"
    key    = "fiap-tech-challenge-terraform/terraform.tfstate"
    region = "us-east-1"
  }


}
provider "aws" {
  region = var.regionDefault
}


provider "kubernetes" {
  host                   = module.eks.endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority)
  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    # Specify cluster name dynamically
    args = ["eks", "get-token", "--cluster-name", module.eks.cluster_name]
  }
}
