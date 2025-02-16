terraform {
  backend "s3" {
    bucket = "ecr-product-service"
    key    = "ecr-product-service/terraform.tfstate"
    region = "us-east-1"
  }


}
provider "aws" {
  region = var.regionDefault
}



