#!/usr/bin/env python

# Prints out the workspace ID of workspaces idle for over "threshold" days (defaults to 50).

import  boto3, csv, os
from datetime import datetime, timedelta
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from botocore.exceptions import ClientError
import time
import logging
log = logging.getLogger()

days = int(os.environ['DAYS'])

def is_idle_workspace(workspace_id, start_date, today):  
    cloudwatch = boto3.client('cloudwatch')
    """Return true if the UserConnected count == 0 for threshold days."""
    metrics = cloudwatch.get_metric_statistics(
        Namespace='AWS/WorkSpaces',
        MetricName='UserConnected',
        Dimensions=[{'Name': 'WorkspaceId', 'Value': workspace_id}],
        Period=1728000,  # every hour
        StartTime=start_date,
        EndTime=today,
        Statistics=['Maximum'],
        Unit='Count'
    )

    if len(metrics):
        for metric in metrics['Datapoints']:
            if metric['Maximum'] != 0:
                return False
        
        return True
    else:
        return False

def get_workspaces(next_token = ''):
    """Get all workspaces, uses recursion to deal with NextTokens."""
    ws = boto3.client('workspaces')
    all_workspaces = []
    if next_token == '':
        workspaces = ws.describe_workspaces()
    else:
        workspaces = ws.describe_workspaces(NextToken=next_token)

    all_workspaces += workspaces['Workspaces']
    if 'NextToken' in workspaces:
        time.sleep(1)
        all_workspaces += get_workspaces(workspaces['NextToken'])

    return all_workspaces


def email(reciver_email, sender_email, region, messege_content):
    messege = build_email(
        "Idle workspaces (0 connected users)",reciver_email, sender_email, body=f"{messege_content}"
    )  # subject, to, from, text
    try:
        send_email(messege, region)
        print("run email")

    except BaseException as e:
        print(e)



def build_email(subject, to_email, from_email, body=None, attachments={}):
    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["To"] = ",".join(to_email) if isinstance(to_email, list) else to_email
    msg["From"] = from_email

    if body and isinstance(body, dict):
        textual_message = MIMEMultipart("alternative")
        for m_type, message in body.items():
            part = MIMEText(message, m_type)
            textual_message.attach(part)
        msg.attach(textual_message)
    elif body and isinstance(body, str):
        msg.attach(MIMEText(body))

    if attachments:
        for filename, data in attachments.items():
            att = MIMEApplication(data)
            att.add_header("Content-Disposition", "attachment", filename=filename)
            msg.attach(att)

    return msg


def send_email(msg, region, session=boto3):
    ses = session.client("ses", region_name=region)
    try:
        response = ses.send_raw_email(
            Source=msg["From"],
            Destinations=msg["To"].split(","),
            RawMessage={"Data": msg.as_string()},
        )
    except ClientError as e:
        log.error(e.response["Error"]["Message"])
    else:
        id = response["MessageId"]
        log.info(f"Email sent! Message ID: {id}")


    
def lambda_handler(event, context):
    email_region = os.environ['REGION']
    reciver_email = os.environ['RECIVER_EMAIL']
    sender_email = os.environ['SENDER_EMAIL']
    send_email = os.environ['SEND_EMAIL']
    email_data = []
    today           = datetime.now() + timedelta(days=1) # today + 1 because we want all of today  
    threshold       = timedelta(days=days)  
    start_date      = today - threshold
    
    all_workspaces = get_workspaces()
    for workspace in all_workspaces:
            if is_idle_workspace(workspace['WorkspaceId'], start_date, today):
                idle = 'TRUE'
                print(f"Idle workspaces (0 connected users for {days} days) ID : {workspace['WorkspaceId']}")
                email_data.append(workspace['WorkspaceId'])
            else:
                idle = 'FALSE'

    if send_email== True:
        email(reciver_email, sender_email, email_region, email_data)
