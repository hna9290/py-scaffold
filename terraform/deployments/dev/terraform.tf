terraform {
  backend "s3" {
    key = "hardik/store-pick/terraform.tfstate"
    region = "eu-west-1"
    encrypt = true
  }
}

