import boto3
import pandas as pd
import sys

def get_security_groups(session, all_regions):
    all_sg = []
    for region in all_regions:
        ec2 = session.resource('ec2', region_name=region)
        sg_list = ec2.security_groups.all()
        for sg in sg_list:
            all_sg.append(sg)
    return all_sg

def extract_sg_details(all_sg):
    sg_details = []
    for sg in all_sg:
        sg_dict = {
            'Region': sg.meta.client.meta.region_name,  # Correctly get the region from the security group's meta data
            'VPC ID': sg.vpc_id,
            'Security Group ID': sg.id,
            'Security Group Name': sg.group_name,
            'Inbound Rules': [],
            'Outbound Rules': []
        }
        
        # Process inbound rules
        for rule in sg.ip_permissions:
            rule_dict = process_sg_rule(rule)
            sg_dict['Inbound Rules'].append(rule_dict)

        # Process outbound rules
        for rule in sg.ip_permissions_egress:
            rule_dict = process_sg_rule(rule)
            sg_dict['Outbound Rules'].append(rule_dict)

        sg_details.append(sg_dict)

    return sg_details

def process_sg_rule(rule):
    protocol = rule['IpProtocol']
    from_port = rule.get('FromPort', 'All')
    to_port = rule.get('ToPort', 'All')
    ip_ranges = [ip_range['CidrIp'] for ip_range in rule['IpRanges']]

    return {'Protocol': protocol, 'From Port': from_port, 'To Port': to_port, 'IP Ranges': ip_ranges}

def save_to_excel(sg_details):
    # Export the security group details to an Excel file
    df = pd.DataFrame(sg_details)
    df.to_excel('security_groups.xlsx', index=False)

def main():
    if len(sys.argv) != 3:
        print("Usage: python script_name.py AWS_profile [AWS_REGION | all]")
        sys.exit(1)

    aws_profile = sys.argv[1]
    aws_region = sys.argv[2]

    session = boto3.Session(profile_name=aws_profile)
    
    # Handle 'all' regions separately
    if aws_region.lower() == 'all':
        ec2_client = session.client('ec2', region_name='us-east-1')
        all_regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    else:
        all_regions = [aws_region]

    all_sg = get_security_groups(session, all_regions)
    sg_details = extract_sg_details(all_sg)
    save_to_excel(sg_details)

if __name__ == "__main__":
    main()