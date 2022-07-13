//To prevent automatic upgrades to new major versions that may contain breaking
//changes, it is recommended to add version = "..." constraints to the
//corresponding provider blocks in configuration, with the constraint strings
//suggested below.
//
//* provider.aws: version = "~> 1.0"
//~> 1.2.0: any non-beta version >= 1.2.0 and < 1.3.0, e.g. 1.2.X

provider "aws" {
  region = var.region
  version = "~> 2.7"
  profile = var.profile
}

provider "random" {
  version = "~> 2.1"
}
