import boto3
import pandas as pd
import sys

def find_orphaned_resources(session, regions):
    orphaned_snapshots = []
    orphaned_volumes = []
    unused_amis = []

    for region in regions:
        ec2_region = session.client('ec2', region_name=region)
        cloudwatch_region = session.client('cloudwatch', region_name=region)  # Create CloudWatch client for each region

        # Process snapshots, volumes, and AMIs in the region
        orphaned_snapshots += process_snapshots(ec2_region)
        orphaned_volumes += process_volumes(ec2_region)
        unused_amis += process_amis(ec2_region, cloudwatch_region)  # Pass the region-specific CloudWatch client

    return orphaned_snapshots, orphaned_volumes, unused_amis

def process_snapshots(ec2_region):
    snapshots = ec2_region.describe_snapshots(OwnerIds=['self'])['Snapshots']
    return [[ec2_region.meta.region_name, snapshot['SnapshotId'], snapshot['StartTime'].replace(tzinfo=None)] 
            for snapshot in snapshots if 'in-use' not in snapshot['State']]

def process_volumes(ec2_region):
    volumes = ec2_region.describe_volumes()['Volumes']
    return [[ec2_region.meta.region_name, volume['VolumeId'], volume['CreateTime'].replace(tzinfo=None)] 
            for volume in volumes if volume['State'] == 'available']

def process_amis(ec2_region, cloudwatch):
    amis = ec2_region.describe_images(Owners=['self'])['Images']
    unused_amis = []
    for ami in amis:
        metrics = cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='StatusCheckFailed_Instance',
            Dimensions=[{'Name': 'ImageId', 'Value': ami['ImageId']}],
            StartTime=pd.Timestamp.utcnow() - pd.Timedelta(days=90),
            EndTime=pd.Timestamp.utcnow(),
            Period=86400,
            Statistics=['Sum']
        )['Datapoints']
        if len(metrics) == 0 or metrics[0]['Sum'] == 0:
            unused_amis.append([ec2_region.meta.region_name, ami['ImageId'], pd.Timestamp(ami['CreationDate']).replace(tzinfo=None)])
    return unused_amis

def save_to_excel(orphaned_snapshots, orphaned_volumes, unused_amis):
    orphaned_snapshots_df = pd.DataFrame(orphaned_snapshots, columns=['Region', 'SnapshotId', 'StartTime'])
    orphaned_volumes_df = pd.DataFrame(orphaned_volumes, columns=['Region', 'VolumeId', 'CreateTime'])
    unused_amis_df = pd.DataFrame(unused_amis, columns=['Region', 'ImageId', 'CreationDate'])

    writer = pd.ExcelWriter('aws_orphans.xlsx', engine='xlsxwriter')
    orphaned_snapshots_df.to_excel(writer, sheet_name='Orphaned Snapshots', index=False)
    orphaned_volumes_df.to_excel(writer, sheet_name='Orphaned Volumes', index=False)
    unused_amis_df.to_excel(writer, sheet_name='Unused AMIs', index=False)
    writer.close()

def main():
    if len(sys.argv) != 3:
        print("Usage: python script_name.py AWS_profile [AWS_REGION | all]")
        sys.exit(1)

    aws_profile = sys.argv[1]
    aws_region = sys.argv[2]

    session = boto3.Session(profile_name=aws_profile)

    if aws_region.lower() == 'all':
        ec2 = session.client('ec2', region_name='us-east-1')  # Set a default region to list all regions
        regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
    else:
        regions = [aws_region]

    orphaned_snapshots, orphaned_volumes, unused_amis = find_orphaned_resources(session, regions)
    save_to_excel(orphaned_snapshots, orphaned_volumes, unused_amis)

if __name__ == "__main__":
    main()
