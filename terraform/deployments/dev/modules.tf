data "terraform_remote_state" "account" {
  backend = "s3"
  workspace = var.environment

  config = {
    bucket = var.state_bucket
    key = "people/store-pick/account/terraform.tfstate"
    region = var.region
    profile = var.profile
  }
}


module "alb" {
  source = "../modules/mor-terraform-aws-modules/elb/alb-lb-nosg"
  vpc-seq-id = var.threeDigitSeqId
  region-id = var.shortRegionDescription
  environment = var.environment
  owner = var.domain
  applicationService = var.shortServiceName
  applicationRole = "${var.serviceName} ALB"
  seq-id = var.environment
  internal-loadbalancer = false
  enable-deletion-protection = false
  cluster = "n"
  build-date = var.build_date
  resource-maintenance-day = "Sun"
  resource-maintenance-time = "Sun:01:00-Sun:03:00"
  project = "shared"
  confidentiality = "High Confidential"
  compliance = "PCI"
  securitygroup-id = var.securityGroup
}


module "alb-tg" {
  source = "../modules/mor-terraform-aws-modules/elb/alb-tg"
  applicationRole = "${var.serviceName} targetgroup"
  alb-tg-port = 80
  alb-tg-protocol = "HTTP"
  deregistration-delay = 30
  target_type = "instance"
  seq-id = var.threeDigitSeqId
  cluster = "n/a"
  applicationService = var.shortServiceName
  environment = var.environment
  build-date = var.build_date
  businessUnit = var.domain
  owner = var.domain
  resource-maintenance-day = "sun"
  resource-maintenance-time = "0300"
  project = "shared"
  region-id = var.shortRegionDescription
  confidentiality = "private"
  compliance = "data"
  vpc-seq-id = var.threeDigitSeqId
  path = var.healthCheckPath
}


module "alb-listener-rule" {
  source = "../modules/mor-terraform-aws-modules/elb/alb-listener-certificate"
  certificate-domain-name = var.route53DomainName
  target-group-arn = module.alb-tg.alb-tg-arn
  lb-arn = module.alb.alb-arn
}


module "aws_cloudwatch_log_group" {
  source = "../modules/mor-terraform-aws-modules/cloudwatch/cloudwatch-log-group"
  confidentiality = "private"
  cluster = "n"
  compliance = "data"
  applicationRole = "${var.serviceName}loggroup"
  applicationService = var.shortServiceName
  build-date = var.build_date
  businessUnit = var.domain
  resource-maintenance-day = "sun"
  resource-maintenance-time = "0300"
  environment = var.environment
  owner = var.domain
  project = "shared"
  seq-id = var.threeDigitSeqId
  region-id = var.shortRegionDescription
}


resource "aws_ecs_task_definition" "task" {
  family = "${var.shortServiceName}-${var.environment}-${var.threeDigitSeqId}"

  container_definitions = <<EOF
[{
	"name": "${var.shortServiceName}-${var.environment}-${var.threeDigitSeqId}",
	"image": "${data.terraform_remote_state.account.outputs.ecr_repo_name}:${var.environment}",
	"cpu": ${var.taskCpu},
	"memory": ${var.taskMemory},
	"memoryReservation": ${var.taskMemoryReservation},
    "privileged": true,
	"portMappings": [{
		"containerPort": ${var.containerPort},
		"hostPort": 0,
		"protocol": "tcp"
	}],
	"essential": true,
	"mountPoints": [],
	"logConfiguration": {
		"logDriver": "awslogs",
		"options": {
			"awslogs-group": "clg-euw1-${var.environment}-${var.domain}-${var.shortServiceName}-${var.threeDigitSeqId}",
			"awslogs-region": "${var.region}",
			"awslogs-stream-prefix": "clg-euw1-${var.environment}-${var.domain}-${var.shortServiceName}-${var.threeDigitSeqId}"
		}
	}
}]
EOF
}


resource "aws_ecs_service" "menu_converter" {
  name = "${var.shortServiceName}-${var.environment}-${var.threeDigitSeqId}"
  cluster = var.cluster
  task_definition = aws_ecs_task_definition.task.arn
  desired_count = 1
  deployment_minimum_healthy_percent = 50
  deployment_maximum_percent = 200
  launch_type = "EC2"
  iam_role = var.role_arn
  load_balancer {
    target_group_arn = module.alb-tg.alb-tg-arn
    container_name = "${var.shortServiceName}-${var.environment}-${var.threeDigitSeqId}"
    container_port = var.containerPort
  }
}


resource "aws_route53_record" "main" {
  zone_id = var.hostedZoneId
  name = "${var.shortServiceName}.${var.environment}"
  type = "CNAME"
  ttl = "10"

  weighted_routing_policy {
    weight = "100"
  }

  set_identifier = var.environment
  records = [
    module.alb.alb-dns-name]
}
