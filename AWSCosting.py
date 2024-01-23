import boto3
import datetime
import pandas as pd
import sys

def get_cost_data(session, start, end, regions):
    ce = session.client('ce')
    data = []

    for region in regions:
        query = {
            "TimePeriod": {"Start": start.strftime('%Y-%m-%d'), "End": end.strftime('%Y-%m-%d')},
            "Granularity": "MONTHLY",
            "Filter": {"Dimensions": {"Key": "REGION", "Values": [region]}},
            "Metrics": ["UnblendedCost"],
            "GroupBy": [{"Type": "DIMENSION", "Key": "SERVICE"}]
        }
        
        result = ce.get_cost_and_usage(**query)
        
        for group in result['ResultsByTime'][0]['Groups']:
            service = group['Keys'][0]
            cost = float(group['Metrics']['UnblendedCost']['Amount'])
            data.append([region, service, cost])

    return data

def save_to_excel(data):
    df = pd.DataFrame(data, columns=['Region', 'Service', 'Cost in SGD'])
    writer = pd.ExcelWriter('aws_costs.xlsx', engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.close()

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <aws_profile_name> <aws_region_name_or_all>")
        sys.exit(1)

    profile_name = sys.argv[1]
    region_name = sys.argv[2]
    
    session = boto3.Session(profile_name=profile_name)

    if region_name.lower() == 'all':
        # Use a default region to create the EC2 client for listing all regions
        ec2 = session.client('ec2', region_name='us-east-1')
        regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
    else:
        regions = [region_name]

    start = datetime.date.today().replace(day=1)
    end = datetime.date.today()

    data = get_cost_data(session, start, end, regions)
    save_to_excel(data)

if __name__ == "__main__":
    main()

# This script first sets up a Boto3 client for the AWS Cost Explorer service
# which is used to retrieve billing information. It then sets the start and end dates for the cost report 
# (in this case, the start of the current month and today's date).
# Next, the script retrieves a list of AWS regions using the Boto3 client for the EC2 service. 
# It then iterates over each region and sets up a query for the Cost Explorer service to retrieve cost data for that region. 
# The query filters the results to only include costs for the current month and for the specified region.
# The script then retrieves the cost data using the Cost Explorer client 
# and prints out the region and cost data for each service in that region.
# Finally, it prints a blank line to separate the output for each region.
# Note that you will need to have AWS credentials set up for this script to work.
# You can set up credentials by following the instructions in the AWS documentation: 
# https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html
# may need to install ----- pip install pandas xlsxwriter