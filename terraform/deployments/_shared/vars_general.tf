## General
variable "environment" {
  description = "The name of the environment"
}

variable "region" {
  default = "eu-west-1"
  description = "Region to deploy on AWS"
}

variable "shortRegionDescription" {
  default = "euw1"
  description = "Short region name"
}

variable "profile" {}

variable "state_bucket" {}
