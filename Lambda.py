import boto3
import pandas as pd
import sys
from datetime import datetime, timedelta

def get_lambda_functions(session, all_aws_regions):
    lambda_functions = []
    # Initialize the AWS Lambda client
    for region in all_aws_regions:
        lambda_client = session.client('lambda', region_name=region)
        functions = lambda_client.list_functions()['Functions']
        for function in functions:
            lambda_client = boto3.client('lambda', region_name=region)
            functions = lambda_client.list_functions()['Functions']
            for function in functions:
                function_name = function['FunctionName']
                memory_size_bytes = function['MemorySize']
                memory_size_mb = memory_size_bytes / 1024  # Convert memory size to MB
                cpu_allocated = function.get('PackageType', 'Not specified')
                provisioned_concurrency = function.get('ProvisionedConcurrencyConfig', {}).get('ProvisionedConcurrentExecutions', 'Not enabled')
                function_concurrency = function.get('Concurrency', {}).get('ReservedConcurrentExecutions', 'Not enabled')
                in_memory_data = function.get('InMemorySizeInMB', 'NA')

            # Calculate the cost of the Lambda function for the last 30 days
            cost = calculate_lambda_cost(session, function_name, region)

            lambda_functions.append({
                'FunctionName': function_name,
                'Region': region,
                'MemoryAllocated in MB': memory_size_mb,
                'CPUAllocated': cpu_allocated,
                'ProvisionedConcurrency': provisioned_concurrency,
                'FunctionConcurrency': function_concurrency,
                'InMemoryData': in_memory_data,
                'CostLast30Days': cost
            })

    return lambda_functions

def calculate_lambda_cost(session, function_name, region):
    # Initialize the AWS Cost Explorer client
    cost_explorer_client = session.client('ce', region_name=region)

    # Calculate the start and end dates for the last 30 days
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=90)

    # Format dates in the required format for Cost Explorer
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # Get the cost and usage for the Lambda function in the last 30 days
    response = cost_explorer_client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date_str,
            'End': end_date_str
        },
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
        GroupBy=[
            {
                'Type': 'TAG',
                'Key': 'lambda_function_name'
            }
        ]
    )

    # Extract the cost value for the specific Lambda function from the response
    for result in response['ResultsByTime']:
        for group in result['Groups']:
            if group['Keys'][0] == function_name:
                cost = group['Metrics']['UnblendedCost']['Amount']
                return cost

    return 'NA'

def get_all_regions(session):
    """Retrieve all AWS regions."""
    ec2 = session.client('ec2', region_name='us-east-1')
    return [region['RegionName'] for region in ec2.describe_regions()['Regions']]

def save_to_excel(lambda_functions):
    # Create a DataFrame using pandas
    df = pd.DataFrame(lambda_functions)

    # Save DataFrame to an Excel file
    df.to_excel('lambda_function_report.xlsx', index=False)

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <aws_profile_name> <aws_region_name_or_all>")
        sys.exit(1)

    aws_profile = sys.argv[1]
    region_name = sys.argv[2]
    session = boto3.Session(profile_name=aws_profile)

    if region_name.lower() == 'all':
        all_aws_regions = get_all_regions(session)
    else:
        all_aws_regions = [region_name]

    lambda_functions = get_lambda_functions(session, all_aws_regions)
    save_to_excel(lambda_functions)

if __name__ == "__main__":
    main()