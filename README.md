# Gets Idle AWS Workspaces

Prints to console workspace_id's that have had 0 userconnection events for "threshold" days, defaults to 50.

Writes out to console and to csv.
The CSV will contain all workspaces, with the IdleFor<THRESHOLD>days header set to either 'TRUE' or 'FALSE'.

## Usage:
```shell
python get_unused_workspaces.py --threshold_days=120
```


## Requirements:
* Must have permission list/describe Workspaces
* Must have permission to get cloudwatch metrics
* boto3 installed
* python3 installed
* aws CLI configured




# Lambda Preventer
```
The script schedules the review of any ebs volumes that have been unattached for X days (deafult 7). 
This reviews all regions in your account
```

## Usage


module "aws_tf_ebs_volumes_cleaner" {
  source = "/aws_tf_ebs_volumes_cleaner"
}

## Optional Inputs

| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| ebs\_volumes\_cleanup\_cron | Rate expression for when to run the review of volumes| string | `"cron(0 7 ? * MON-FRI *)"` | no 
| function\_prefix | Prefix for the name of the lambda created | string | `""` | no |
| days| The number of days the Snapshot has been there and so will no be deleted | `"7"` | no |


## Testing 

Configure your AWS credentials using one of the [supported methods for AWS CLI
   tools](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html), such as setting the
   `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables. If you're using the `~/.aws/config` file for profiles then export `AWS_SDK_LOAD_CONFIG` as "True".
1. Install [Terraform](https://www.terraform.io/) and make sure it's on your `PATH`.
1. Install [Golang](https://golang.org/) and make sure this code is checked out into your `GOPATH`.
cd test
go mod init github.com/sg/sch
go test -v -run TestTerraformAwsExample