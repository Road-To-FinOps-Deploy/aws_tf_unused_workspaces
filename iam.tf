resource "aws_iam_role" "iam_role_for_unused_workspaces" {
  name               = "${var.function_prefix}role_for_unused_workspaces"
  assume_role_policy = file("${path.module}/policies/LambdaAssume.pol")
}

resource "aws_iam_role_policy" "iam_role_policy_for_unused_workspaces" {
  name   = "${var.function_prefix}policy_for_unused_workspaces"
  role   = aws_iam_role.iam_role_for_unused_workspaces.id
  policy = file("${path.module}/policies/LambdaExecution.pol")
}

resource "aws_iam_policy" "workspace_policy" {
  name        = "${var.function_prefix}workspace_policy"
  path        = "/"
  description = "Policy to force owner to add tag to EC2"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
    "Sid": "VisualEditor0",
    "Effect": "Allow",
    "Action": "workspaces:*",
    "Resource": "*"
    }
  ]
}
EOF

}

