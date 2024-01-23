import boto3
import csv
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <aws_profile_name> <aws_region_name_or_all>")
        sys.exit(1)

    profile_name = sys.argv[1]
    region_name = sys.argv[2]
    session = boto3.Session(profile_name=profile_name)

    if region_name.lower() == 'all':
        ec2_cli = session.client('ec2', region_name='us-east-1')
        all_aws_regions = [region['RegionName'] for region in ec2_cli.describe_regions()['Regions']]
    else:
        all_aws_regions = [region_name]

    with open('volume_inventory.csv', 'w', newline='') as file_open:
        data_obj = csv.writer(file_open)
        # ... write headers ...

        for each_region in all_aws_regions:
            ec2_resource = session.resource(service_name='ec2', region_name=each_region)
            for volume in ec2_resource.volumes.all():
                # Get volume tags and other details
                volume_tags = ", ".join([f"{tag['Key']}={tag['Value']}" for tag in volume.tags]) if volume.tags else ""
                has_snapshots = 'Yes' if list(volume.snapshots.all()) else 'No'
                attached_instance = volume.attachments[0]['InstanceId'] if volume.attachments else ""

                # Calculate utilized size for gp2 and io1 volumes
                utilized_size_gb = 0
                if volume.volume_type in ['gp2', 'io1']:
                    cloudwatch = boto3.client('cloudwatch', region_name=each_region)
                    response = cloudwatch.get_metric_statistics(
                        Namespace='AWS/EBS',
                        MetricName='VolumeWriteBytes',
                        Dimensions=[{'Name': 'VolumeId', 'Value': volume.id}],
                        StartTime='2023-07-01T00:00:00Z',
                        EndTime='2023-07-25T23:59:59Z',
                        Period=86400,
                        Statistics=['Average'],
                        Unit='Bytes'
                    )
                    if response['Datapoints']:
                        utilized_size_gb = response['Datapoints'][0]['Average'] / (1024 ** 3)

                # Write volume details to the CSV file
                data_obj.writerow([
                    volume.id, volume.size, volume.state, volume.volume_type,
                    volume_tags, volume.availability_zone, each_region, has_snapshots, attached_instance, utilized_size_gb
                ])

            # Retrieve information about EC2 instances in the region
            instances = ec2_resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
            for instance in instances:
                for block_device in instance.block_device_mappings:
                    if 'Ebs' not in block_device:
                        data_obj.writerow([
                            block_device['DeviceName'], "Instance Store", "Attached", "Instance Store",
                            "", "", each_region, "N/A", instance.id, "N/A"
                        ])

if __name__ == "__main__":
    main()