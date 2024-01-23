import boto3
import pandas as pd
import sys

def get_s3_bucket_objects_count(bucket_name, s3_client):
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    count = response.get('KeyCount', 0)
    return count

def get_all_s3_buckets(s3_client):
    response = s3_client.list_buckets()
    buckets = response['Buckets']
    return buckets

def get_read_heavy_buckets(storage_lens_client, account_id):
    read_heavy_buckets = []
    try:
        response = storage_lens_client.list_storage_lens_configurations(AccountId=account_id)
        configurations = response['StorageLensConfigurations']
        for config in configurations:
            if config['LensType'] == 'Organization':
                read_heavy_buckets.extend(config['BucketLevel']['ActivityMetrics']['ReadIOBytes']['Bucket'])
    except KeyError:
        pass
    return read_heavy_buckets

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <aws_profile_name> <aws_region_name>")
        sys.exit(1)

    aws_profile = sys.argv[1]
    region_name = sys.argv[2]

    # Initialize AWS clients using AWS profile and region
    session = boto3.Session(profile_name=aws_profile)
    sts_client = session.client('sts', region_name='us-east-1')
    s3_client = session.client('s3')
    storage_lens_client = session.client('s3control', region_name='us-east-1')

    # Get AWS account ID
    account_id = sts_client.get_caller_identity().get('Account')

    # Get all S3 buckets
    buckets = get_all_s3_buckets(s3_client)

    # Calculate object counts for each bucket
    bucket_object_counts = {bucket['Name']: get_s3_bucket_objects_count(bucket['Name'], s3_client) for bucket in buckets}

    # Create a Pandas DataFrame with bucket names and object counts
    df = pd.DataFrame(list(bucket_object_counts.items()), columns=['Bucket Name', 'Object Count'])

    # Save the DataFrame to an Excel file
    output_file = 's3_bucket_objects.xlsx'
    df.to_excel(output_file, index=False)

    # Get read-heavy buckets
    read_heavy_buckets = get_read_heavy_buckets(storage_lens_client, account_id)

    # Create a Pandas DataFrame with read-heavy bucket names
    df_read_heavy = pd.DataFrame(read_heavy_buckets, columns=['Read-Heavy Buckets'])

    # Save the DataFrame to the same Excel file, in a separate sheet
    with pd.ExcelWriter(output_file, engine='openpyxl', mode='a') as writer:
        df_read_heavy.to_excel(writer, sheet_name='Read-Heavy Buckets', index=False)

if __name__ == "__main__":
    main()
