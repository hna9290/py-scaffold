#Genric tags
variable "businessUnit" {
  default = "People"
}

variable "resource-maintenance-day" {
  default = "sun"
}

variable "resource-maintenance-time" {
  default = "0300"
}

variable "project" {
  default = "storepick"
}

variable "serviceName" {
  default = "menu-converter"
}

variable "confidentiality" {
  default = "private"
}

variable "compliance" {
  default = "data"
}

variable "domain" {
  description = "The name of the tower/stack and owner, e.g. infra, retail"
  default = "people"
}

variable "cluster" {
}

variable "shortServiceName" {
  default = "menu_converter"
}

variable "build_date" {}

variable "threeDigitSeqId" {}