#!/usr/bin/env python

# Prints out the workspace ID of workspaces idle for over "threshold" days (defaults to 50).

import argparse, boto3, csv
from datetime import datetime, timedelta
import time

parser = argparse.ArgumentParser()
parser.add_argument("--threshold_days", nargs='?', default=50, type=int,
                    help="Idle Workspaces threshold in days, defaults to 50.")

args = parser.parse_args()
threshold_days = args.threshold_days

def is_idle_workspace(workspace_id, start_date, today):  
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

today           = datetime.now() + timedelta(days=1) # today + 1 because we want all of today  
threshold       = timedelta(days=threshold_days)  
start_date      = today - threshold

cloudwatch = boto3.client('cloudwatch')
ws = boto3.client('workspaces')

all_workspaces = get_workspaces()

with open('workspaces.csv', 'w') as out_file:
    writer = csv.writer(out_file)
    idle_header=f'IdleFor{threshold_days}Days'
    writer.writerow(["WorkspaceId", "UserName", "State", "RunningMode", idle_header])

    print(f'Idle workspaces (0 connected users for {threshold_days} days):')
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
    