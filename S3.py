import boto3
import pandas as pd
from botocore.exceptions import ClientError
import sys

def get_s3_bucket_info(profile_name):
    session = boto3.Session(profile_name=profile_name)
    s3_client = session.client('s3')
    
    data = {
        "Name": [],
        "Region": [],
        "Size (GB)": [],
        "Versioning Enabled": [],
        "Encryption Enabled": [],
        "Storage Class": [],
        "Intelligent Tiering Enabled": [],
        "Object Lock Enabled": [],
        "Tag": []
    }

    for bucket in s3_client.list_buckets()['Buckets']:
        bucket_name = bucket['Name']
        try:
            bucket_region = s3_client.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
            if bucket_region is None:
                bucket_region = 'us-east-1'

            region_specific_s3_client = boto3.client('s3', region_name=bucket_region)

            # Get bucket size
            bucket_size = 0
            response = region_specific_s3_client.list_objects_v2(Bucket=bucket_name)
            for obj in response.get('Contents', []):
                bucket_size += obj['Size']
            bucket_size_gb = bucket_size / (1024**3)

            # Placeholder logic to populate other fields
            versioning_enabled = "No"  # Replace with actual logic
            encryption_enabled = "No"  # Replace with actual logic
            storage_class = "Standard"  # Replace with actual logic
            intelligent_tiering_enabled = "No"  # Replace with actual logic
            object_lock_enabled = "No"  # Replace with actual logic
            tags = ""  # Replace with actual logic

            data["Name"].append(bucket_name)
            data["Region"].append(bucket_region)
            data["Size (GB)"].append(bucket_size_gb)
            data["Versioning Enabled"].append(versioning_enabled)
            data["Encryption Enabled"].append(encryption_enabled)
            data["Storage Class"].append(storage_class)
            data["Intelligent Tiering Enabled"].append(intelligent_tiering_enabled)
            data["Object Lock Enabled"].append(object_lock_enabled)
            data["Tag"].append(tags)
        
        except ClientError as e:
            print(f"Error processing bucket {bucket_name}: {e}")

    # Ensure all columns have the same length
    max_length = max(len(v) for v in data.values())
    for key, value in data.items():
        if len(value) < max_length:
            data[key] += ["NA"] * (max_length - len(value))

    df = pd.DataFrame(data)
    return df

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py AWS_profile")
        sys.exit(1)

    aws_profile = sys.argv[1]

    df = get_s3_bucket_info(aws_profile)

    writer = pd.ExcelWriter('s3_bucket_info.xlsx', engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.book.close()

if __name__ == "__main__":
    main()
