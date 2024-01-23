import boto3
import csv
import sys

def get_all_regions(session):
    """Retrieve all AWS regions."""
    ec2 = session.client('ec2', region_name='us-east-1')
    return [region['RegionName'] for region in ec2.describe_regions()['Regions']]

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <aws_profile_name> <aws_region_name_or_all>")
        sys.exit(1)

    profile_name = sys.argv[1]
    region_name = sys.argv[2]
    session = boto3.Session(profile_name=profile_name)

    if region_name.lower() == 'all':
        all_aws_regions = get_all_regions(session)
    else:
        all_aws_regions = [region_name]

    with open('ec2_inventory.csv', 'w', newline='') as file_open:
        data_obj = csv.writer(file_open)
        data_obj.writerow([
            "S.no", "InstanceID", "ImageID", "Instance Lifecycle", "Instance Type",
            "Private DNS Name", "Private IP Address", "Root Device Name",
            "Root Device Type", "VPC ID", "Availability Zone", "Region",
            "Number of NICs", "Has Elastic IP", "Security Groups"
        ])

        count = 1
        for each_region in all_aws_regions:
            ec2_resource = session.resource(service_name='ec2', region_name=each_region)
            for each_inst_in_reg in ec2_resource.instances.all():
                security_groups = [sg['GroupName'] for sg in each_inst_in_reg.security_groups]
                num_nics = len(each_inst_in_reg.network_interfaces)
                has_elastic_ip = "Yes" if each_inst_in_reg.public_ip_address else "No"

                data_obj.writerow([
                    count, each_inst_in_reg.instance_id, each_inst_in_reg.image_id,
                    each_inst_in_reg.instance_lifecycle, each_inst_in_reg.instance_type,
                    each_inst_in_reg.private_dns_name, each_inst_in_reg.private_ip_address,
                    each_inst_in_reg.root_device_name, each_inst_in_reg.root_device_type,
                    each_inst_in_reg.vpc_id, each_inst_in_reg.placement['AvailabilityZone'],
                    each_region, num_nics, has_elastic_ip, ", ".join(security_groups)
                ])
                count += 1

if __name__ == "__main__":
    main()
