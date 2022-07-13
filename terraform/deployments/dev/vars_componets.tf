variable "seq-id" {}

variable "application_role" {
  description = "The name of the application role, e.g. app_server"
}

variable "application_service" {
  description = "The name of the application service"
}

#Cloudwatch
variable "retention-in-days" {
  default = 30
}

variable "healthCheckPath" {}

variable "route53DomainName" {}

variable "taskCpu" {}
variable "taskMemory" {}
variable "taskMemoryReservation" {}
variable "containerPort" {}
variable "role_arn" {}

variable "hostedZoneId" {}

variable "securityGroup" {
  description = "security group for ALB"
  default = "sg-03483c9d2909f6a6c"
}