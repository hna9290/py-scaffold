args =
tf-command = apply
env = dev

.PHONY: terrafile

terraform:
	echo "yes"|terraform init -var-file=vars/$(env).tfvars -backend-config=conf/$(env).backend.conf
	if terraform workspace list | grep $(env); then terraform workspace select $(env); else terraform workspace new $(env); fi
	terraform $(tf-command) -var-file=vars/$(env).tfvars $(args) -var build_date=`date +%Y-%m-%d`


terraform-destroy:
	terraform workspace select $(env)
	terraform destroy -var-file=vars/$(env).tfvars $(args) -var build_date=`date +%Y-%m-%d`


terrafile:
	pwd
	./terrafile/terrafile.py $(args)
