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