#!/usr/bin/env python

# Prints out the workspace ID of workspaces idle for over "threshold" days (defaults to 50).

import  boto3, csv, os
from datetime import datetime, timedelta
import time


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
    
def lambda_handler(event, context):
    today           = datetime.now() + timedelta(days=1) # today + 1 because we want all of today  
    threshold       = timedelta(days=days)  
    start_date      = today - threshold
    
    all_workspaces = get_workspaces()

    with open('workspaces.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        idle_header=f'IdleFor{days}Days'
        writer.writerow(["WorkspaceId", "UserName", "State", "RunningMode", idle_header])

        print(f'Idle workspaces (0 connected users for {days} days):')
        for workspace in all_workspaces:
            if is_idle_workspace(workspace['WorkspaceId'], start_date, today):
                idle = 'TRUE'
            else:
                idle = 'FALSE'

            writer.writerow(
                [
                    workspace['WorkspaceId'],
                    workspace['UserName'],
                    workspace['State'],
                    workspace['WorkspaceProperties']['RunningMode'],
                    idle
                ]
            )
            print(workspace['WorkspaceId'])
