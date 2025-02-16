terraform {
  backend "s3" {
    bucket = "ecr_product_service"
    key    = "ecr_product_service/terraform.tfstate"
    region = "us-east-1"
  }


}
provider "aws" {
  region = var.regionDefault
}



