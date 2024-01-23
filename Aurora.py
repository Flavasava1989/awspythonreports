import boto3
import pandas as pd
import sys

def get_aurora_database_info(profile_name, region_name):
    session = boto3.Session(profile_name=profile_name)

    if region_name.lower() == 'all':
        regions = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]
    else:
        regions = [region_name]

    data = {
        "Name": [],
        "AZ": [],
        "Region": [],
        "VPC": [],
        "Security Group": [],
        "Size (GB)": [],
        "Utilized Size (GB)": [],
        "Snapshots Enabled": [],
        "No. of Snapshots": [],
        "Database Engine": []
    }

    for region in regions:
        rds_client = boto3.client('rds', region_name=region)
        clusters = rds_client.describe_db_clusters()

        for cluster in clusters['DBClusters']:
            data["Name"].append(cluster['DBClusterIdentifier'])
            data["AZ"].append(cluster['MultiAZ'])
            data["Region"].append(region)
            data["VPC"].append(cluster['VpcId'])
            data["Security Group"].append(', '.join(sg['VpcSecurityGroupId'] for sg in cluster['VpcSecurityGroups']))
            data["Size (GB)"].append(cluster['AllocatedStorage'])
            data["Utilized Size (GB)"].append(cluster['AllocatedStorage'] - cluster['FreeStorage'])
            data["Snapshots Enabled"].append("Yes" if cluster['BackupRetentionPeriod'] > 0 else "No")
            data["No. of Snapshots"].append(len(rds_client.describe_db_cluster_snapshots(DBClusterIdentifier=cluster['DBClusterIdentifier'])['DBClusterSnapshots']))
            data["Database Engine"].append(cluster['Engine'])

    df = pd.DataFrame(data)
    return df

def main():
    if len(sys.argv) != 3:
        print("Usage: python aurora.py <aws_profile_name> <aws_region_name>")
        sys.exit(1)

    profile_name = sys.argv[1]
    region_name = sys.argv[2]

    df = get_aurora_database_info(profile_name, region_name)

    # Write the DataFrame to an Excel file
    writer = pd.ExcelWriter('aurora_database_info.xlsx', engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.book.close()

if __name__ == "__main__":
    main()
