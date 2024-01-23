import boto3
import pandas as pd
import datetime
import sys

def get_all_regions(session):
    """Retrieve all AWS regions."""
    ec2 = session.client('ec2', region_name='us-east-1')
    return [region['RegionName'] for region in ec2.describe_regions()['Regions']]

def get_dynamodb_data_for_region(session, region):
    """Retrieve DynamoDB data for a specific region."""
    client = session.client('dynamodb', region_name=region)
    cloudwatch_client = session.client('cloudwatch', region_name=region)
    table_list = client.list_tables()['TableNames']

    data = []
    for table_name in table_list:
        table_desc = client.describe_table(TableName=table_name)['Table']   
        if 'BillingModeSummary' in table_desc:
            storage_class = table_desc['BillingModeSummary']['BillingMode']
        else:
            storage_class = 'Unknown'
        start_time = datetime.datetime.now() - datetime.timedelta(days=30)
        end_time = datetime.datetime.now()
        
        rcu_stats = cloudwatch_client.get_metric_statistics(
            Namespace='AWS/DynamoDB',
            MetricName='ConsumedReadCapacityUnits',
            Dimensions=[{'Name': 'TableName', 'Value': table_name}],
            StartTime=start_time.isoformat(),
            EndTime=end_time.isoformat(),
            Period=86400,
            Statistics=['Sum']
        )
        wcu_stats = cloudwatch_client.get_metric_statistics(
            Namespace='AWS/DynamoDB',
            MetricName='ConsumedWriteCapacityUnits',
            Dimensions=[{'Name': 'TableName', 'Value': table_name}],
            StartTime=start_time.isoformat(),
            EndTime=end_time.isoformat(),
            Period=86400,
            Statistics=['Sum']
        )

        rcu_consumed = rcu_stats['Datapoints'][0]['Sum'] if rcu_stats['Datapoints'] else 0
        wcu_consumed = wcu_stats['Datapoints'][0]['Sum'] if wcu_stats['Datapoints'] else 0
        backup_list = client.list_backups(TableName=table_name)['BackupSummaries']

        data.append({
            'Table Name': table_name,
            'Storage Class': storage_class,  # Use the variable instead of directly accessing the dictionary
            'Utilized Capacity (GB)': table_desc['TableSizeBytes'] / 1024 / 1024 / 1024,
            'Region': region,
            'RCU Consumed (Last 30 Days)': rcu_consumed,
            'WCU Consumed (Last 30 Days)': wcu_consumed,
            'Scheduled Backups': ', '.join([backup['BackupArn'] for backup in backup_list]) if backup_list else 'No scheduled backups',
            'Unused Tables': 'Unused' if rcu_consumed == 0 and wcu_consumed == 0 else 'Used'
        })

    return data

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <aws_profile_name> <aws_region_name_or_all>")
        sys.exit(1)

    profile_name = sys.argv[1]
    region_name = sys.argv[2]
    session = boto3.Session(profile_name=profile_name)

    if region_name.lower() == 'all':
        regions = get_all_regions(session)
    else:
        regions = [region_name]

    all_data = []
    for region in regions:
        region_data = get_dynamodb_data_for_region(session, region)
        all_data.extend(region_data)

    df = pd.DataFrame(all_data)
    writer = pd.ExcelWriter('dynamodb_report.xlsx', engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.book.close()

if __name__ == "__main__":
    main()
