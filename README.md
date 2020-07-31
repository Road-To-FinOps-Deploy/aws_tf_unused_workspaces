# Gets Idle AWS Workspaces

```
The script schedules the review of any workspaces that have had 0 userconnection events for "threshold" days, defaults to 28. 
This reviews all regions in your account
```

## Usage


module "aws_tf_unused_workspaces" {
  source = "/aws_tf_unused_workspaces"
  send_email = true
  sender_email = "emailer@hotmail.com"
  reciver_email = "emailto@hotmail.com"
}

## Optional Inputs

| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| unused\_workspaces\_cleanup\_cron | Rate expression for when to run the review of volumes| string | `"cron(0 8 1 * ? *)"` | no 
| function\_prefix | Prefix for the name of the lambda created | string | `""` | no |
| days| The number of days the Snapshot has been there and so will no be deleted | `"28"` | no |
| region| Region it is deployed to and emailed from | `"eu-west-1"` | no | 
| send\_email| If you want to recive an email for this report | `"True"` | no |
| sender\_email| If yes to send email the needed. Who will be sending the email| `""` | yes/no |
| reciver\_email| If yes to recive email the needed. Who will be sending the emai| `"28"` | yes/ |

## Testing 

Configure your AWS credentials using one of the [supported methods for AWS CLI
   tools](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html), such as setting the
   `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables. If you're using the `~/.aws/config` file for profiles then export `AWS_SDK_LOAD_CONFIG` as "True".
1. Install [Terraform](https://www.terraform.io/) and make sure it's on your `PATH`.
1. Install [Golang](https://golang.org/) and make sure this code is checked out into your `GOPATH`.
cd test
go mod init github.com/sg/sch
go test -v -run TestTerraformAws