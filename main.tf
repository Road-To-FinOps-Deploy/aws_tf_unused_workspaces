data "archive_file" "unused_workspaces_zip" {
  type        = "zip"
  source_file = "${path.module}/source/unused_workspaces.py"
  output_path = "${path.module}/source/unused_workspaces.zip"
}

resource "aws_lambda_function" "unused_workspaces_cleanup" {
  filename         = "${path.module}/source/unused_workspaces.zip"
  function_name    = "${var.function_prefix}unused_workspaces_cleanup"
  role             = aws_iam_role.iam_role_for_unused_workspaces.arn
  handler          = "unused_workspaces.lambda_handler"
  source_code_hash = data.archive_file.unused_workspaces_zip.output_base64sha256
  runtime          = "python3.6"
  memory_size      = "512"
  timeout          = "150"

  environment {
    variables = {
      DAYS = var.days
    }
  }
}

resource "aws_lambda_permission" "allow_cloudwatch_unused_workspaces_cleanup" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.unused_workspaces_cleanup.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.unused_workspaces_cleanup_cloudwatch_rule.arn
}

resource "aws_cloudwatch_event_rule" "unused_workspaces_cleanup_cloudwatch_rule" {
  name                = "unused_workspaces_cleanup_lambda_trigger"
  schedule_expression = var.unused_workspaces_cleanup_cron
}

resource "aws_cloudwatch_event_target" "unused_workspaces_cleanup_lambda" {
  rule      = aws_cloudwatch_event_rule.unused_workspaces_cleanup_cloudwatch_rule.name
  target_id = "unused_workspaces_cleanup_lambda_target"
  arn       = aws_lambda_function.unused_workspaces_cleanup.arn
}

