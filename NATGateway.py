import boto3
from datetime import datetime, timedelta
import pandas as pd
import sys

def get_nat_gateways_info(region_name, profile_name):
    session = boto3.Session(profile_name=profile_name)
    if region_name.lower() == 'all':
        # If the region is 'all', list all regions
        client = session.client('ec2', region_name='us-east-1')  # Set a default region to list all regions
        regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    else:
        # If a specific region is provided
        regions = [region_name]

    nat_gateways = []

    for region in regions:
        session = boto3.Session(profile_name=profile_name, region_name=region)
        client = session.client('ec2')
        ec2 = session.resource('ec2', region_name=region)

        for nat_gateway in client.describe_nat_gateways()['NatGateways']:
            vpc = ec2.Vpc(nat_gateway['VpcId'])
            subnet = ec2.Subnet(nat_gateway['SubnetId'])

            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=30)
            data_usage = client.get_nat_gateway_statistics(
                NatGatewayId=nat_gateway['NatGatewayId'],
                StartTime=start_time,
                EndTime=end_time
            )['NatGatewayStatistics'][0]['BytesOutFromNatGateway']

            data_usage_gb = round(data_usage / (1024**3), 2)

            nat_gateways.append({
                'Name': nat_gateway['NatGatewayId'],
                'Region': region,
                'Subnet': subnet.cidr_block,
                'Data Usage (GB)': data_usage_gb
            })

    return pd.DataFrame(nat_gateways)

def main():
    if len(sys.argv) != 3:
        print("Usage: python NATGateway.py AWS_profile [AWS_REGION | all]")
        sys.exit(1)

    aws_profile = sys.argv[1]
    aws_region = sys.argv[2]

    df = get_nat_gateways_info(aws_region, aws_profile)
    df.to_excel('nat_gateways.xlsx', index=False)

if __name__ == "__main__":
    main()
