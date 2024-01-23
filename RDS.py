import boto3
import pandas as pd
import sys

def get_rds_database_info(profile_name, region_name):
    session = boto3.Session(profile_name=profile_name)

    if region_name.lower() == 'all':
        ec2 = session.client('ec2', region_name='us-east-1')  # Set a default region to list all regions
        regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
    else:
        regions = [region_name]

    data = {
        "Name": [],
        "AZ": [],
        "Region": [],
        "VPC": [],
        "Security Group": [],
        "Database Engine": [],
        "Size (GB)": [],
        "Utilized Size (GB)": [],
        "Snapshots Enabled": [],
        "No. of Snapshots": []
    }

    for region in regions:
        rds_client = session.client('rds', region_name=region)

        instances = rds_client.describe_db_instances()

        for instance in instances['DBInstances']:
            data["Name"].append(instance['DBInstanceIdentifier'])
            data["AZ"].append(instance['AvailabilityZone'])
            data["Region"].append(region)
            data["VPC"].append(instance['DBSubnetGroup']['VpcId'])
            data["Security Group"].append(', '.join(sg['VpcSecurityGroupId'] for sg in instance['VpcSecurityGroups']))
            data["Database Engine"].append(instance['Engine'])
            data["Size (GB)"].append(instance['AllocatedStorage'])
            data["Utilized Size (GB)"].append(instance['AllocatedStorage'] - instance['FreeStorageSpace'])
            data["Snapshots Enabled"].append("Yes" if instance['BackupRetentionPeriod'] > 0 else "No")
            data["No. of Snapshots"].append(len(rds_client.describe_db_snapshots(DBInstanceIdentifier=instance['DBInstanceIdentifier'])['DBSnapshots']))

    df = pd.DataFrame(data)
    return df

def main():
    if len(sys.argv) != 3:
        print("Usage: python RDS.py AWS_PROFILE AWS_REGION")
        sys.exit(1)

    aws_profile = sys.argv[1]
    aws_region = sys.argv[2]

    df = get_rds_database_info(aws_profile, aws_region)

    # Write the DataFrame to an Excel file
    writer = pd.ExcelWriter('rds_database_info.xlsx', engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.book.close()

if __name__ == "__main__":
    main()
