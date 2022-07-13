terraform {
  backend "s3" {
    key = "people/store-pick/account/terraform.tfstate"
    region = "eu-west-1"
    encrypt = true
  }
}

module "ecr_rep" {
  source = "../modules/mor-terraform-aws-modules/ecr"
  project = var.project
  name = var.serviceName
}
