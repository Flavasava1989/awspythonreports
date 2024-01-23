import boto3
import pandas as pd
import subprocess
import json
import sys

def get_aws_account_id(profile_name):
    # Use the AWS CLI to get the AWS account ID
    try:
        aws_account_info = subprocess.check_output(['aws', 'sts', 'get-caller-identity', '--profile', profile_name])
        aws_account_info = aws_account_info.decode('utf-8')
        aws_account_info = json.loads(aws_account_info)
        return aws_account_info.get('Account')
    except Exception as e:
        print(f"Error getting AWS account ID: {str(e)}")
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py AWS_profile")
        sys.exit(1)

    aws_profile = sys.argv[1]

    # Create a Boto3 session with the specified profile
    session = boto3.Session(profile_name=aws_profile)
    client = session.client('s3')

    # Get the AWS account ID
    aws_account_id = get_aws_account_id(aws_profile)
    
    if aws_account_id is None:
        print("Failed to get AWS account ID. Exiting...")
        return

    print(f"Starting s3_repl.py for AWS Account ID: {aws_account_id}")

    # List all S3 buckets in the AWS account
    response = client.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response['Buckets']]

    # Initialize a list to store all the rule data
    all_rule_data = []

    # Iterate through each S3 bucket in the list
    for bucket_name in bucket_names:
        try:
            # Get the replication configuration for the current bucket
            response = client.get_bucket_replication(Bucket=bucket_name)
            replication_config = response.get('ReplicationConfiguration')
            rules_list = replication_config.get('Rules', [])
            
            # Skip the bucket if it doesn't have a replication configuration
            if not rules_list:
                print(f"Bucket '{bucket_name}' does not have a replication configuration. Skipping...")
                continue
            
            # Get the region of the source bucket
            source_bucket_region = client.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
            if source_bucket_region is None:
                source_bucket_region = 'us-east-1'  # Set the region to 'us-east-1' for the default region
            
            # Loop through each rule in the 'Rules' list and retrieve the data
            for rule in rules_list:
                rule_id = rule.get('ID')
                rule_status = rule.get('Status')
                rule_priority = rule.get('Priority')
                rule_filter = rule.get('Filter')
                rule_status_remote_bucket_arn = rule.get('Destination', {}).get('Bucket')
                
                # Extract only the bucket name from the ARN
                rule_status_remote_bucket = rule_status_remote_bucket_arn.split(':')[-1]
                
                # Get the region of the destination bucket
                destination_bucket_region = client.get_bucket_location(Bucket=rule_status_remote_bucket)['LocationConstraint']
                
                # Append the data to the all_rule_data list
                all_rule_data.append({
                    'Bucket': bucket_name,
                    'RuleID': rule_id,
                    'Status': rule_status,
                    'Priority': rule_priority,
                    'Filter': rule_filter,
                    'RemoteBucket': rule_status_remote_bucket,
                    'SourceBucketRegion': source_bucket_region,
                    'DestinationBucketRegion': destination_bucket_region
                })
        except Exception as e:
            print(f"Error processing bucket '{bucket_name}': {str(e)}")
            # You can handle other exceptions as needed. For example, you can log the error or continue with the next bucket.

    # Create a DataFrame from the all_rule_data list
    df = pd.DataFrame(all_rule_data)

    # Save the DataFrame to an Excel file
    output_file = "S3replication.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Excel file '{output_file}' generated.")

if __name__ == "__main__":
    main()
