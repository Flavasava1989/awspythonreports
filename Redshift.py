import boto3
import pandas as pd
import sys

def get_redshift_database_info(profile_name, region_name):
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
        "Size (GB)": [],
        "Utilized Size (GB)": [],
        "Snapshots Enabled": [],
        "No. of Snapshots": []
    }

    for region in regions:
        redshift_client = session.client('redshift', region_name=region)
        clusters = redshift_client.describe_clusters()

        for cluster in clusters['Clusters']:
            data["Name"].append(cluster['ClusterIdentifier'])
            data["AZ"].append(cluster['AvailabilityZone'])
            data["Region"].append(region)
            data["VPC"].append(cluster['VpcId'])
            data["Security Group"].append(', '.join(ec2_sg['VpcSecurityGroupId'] for ec2_sg in cluster['VpcSecurityGroups']))
            data["Size (GB)"].append(cluster['ClusterSize'])
            data["Utilized Size (GB)"].append(cluster['TotalResizeDataInMegaBytes'] / 1024)
            data["Snapshots Enabled"].append("Yes" if cluster['AutomatedSnapshotRetentionPeriod'] > 0 else "No")
            data["No. of Snapshots"].append(len(redshift_client.describe_cluster_snapshots(ClusterIdentifier=cluster['ClusterIdentifier'])['Snapshots']))

    df = pd.DataFrame(data)
    return df

def main():
    if len(sys.argv) != 3:
        print("Usage: python script_name.py AWS_profile [AWS_REGION | all]")
        sys.exit(1)

    aws_profile = sys.argv[1]
    aws_region = sys.argv[2]

    df = get_redshift_database_info(aws_profile, aws_region)

    # Write the DataFrame to an Excel file
    writer = pd.ExcelWriter('redshift_database_info.xlsx', engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.book.close()

if __name__ == "__main__":
    main()
