resource "aws_ecr_repository" "ecr_product_service" {
  name                 = "ecr_product_service"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}
