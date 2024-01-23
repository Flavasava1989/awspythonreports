import multiprocessing
import subprocess
import os
import datetime
import functools
import shutil
import sys

def run_python_file(file_name, output_folder, aws_profile, aws_region):
    print(f"Running {file_name} in process ID: {os.getpid()}")
    try:
        # Scripts that require only the AWS profile argument
        profile_only_scripts = ['S3.py', 's3repl_latest.py']

        # Determine the command based on the script being run
        if file_name in profile_only_scripts:
            command = ['python', file_name, aws_profile]
        else:
            command = ['python', file_name, aws_profile, aws_region]

        subprocess.run(command, check=True)
        print(f"Successfully ran {file_name}")
    except Exception as e:
        print(f"Error running {file_name}: {str(e)}")


def reports(file_names):
    print("Available Reports:")
    for i, file_name in enumerate(file_names, 1):
        print(f"{i}. {file_name}")

    print("\nType the number for a specific report, multiple numbers separated by commas for multiple reports, or 'all' for all reports.")
    user_input = input("Your choice: ").strip().lower()

    if user_input == 'all':
        return file_names
    else:
        selected_indices = [int(index.strip()) - 1 for index in user_input.split(',') if index.strip().isdigit()]
        return [file_names[index] for index in selected_indices if index < len(file_names)]

def create_output_folder():
    today = datetime.datetime.now()
    folder_name = f"AWS_Reports_{today.strftime('%d%m%Y')}"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    return folder_name

def move_report_files(output_folder):
    report_files = [
        "aurora_database_info.xlsx",
        "aws_costs.xlsx",
        "volume_inventory.csv",
        "dynamodb_report.xlsx",
        "ec2_inventory.csv",
        "s3_bucket_objects.xlsx",
        "lambda_function_report.xlsx",
        "nat_gateways.xlsx",
        "aws_orphans.xlsx",
        "rds_database_info.xlsx",
        "redshift_database_info.xlsx",
        "s3_bucket_info.xlsx",
        "S3replication.xlsx",
        "security_groups.xlsx",
    ]
    
    for report_file in report_files:
        if os.path.exists(report_file):
            shutil.move(report_file, os.path.join(output_folder, report_file))

def main():
    file_names = [
        "S3.py",
        "Aurora.py",
        "RDS.py",
        "Redshift.py",
        "NATGateway.py",
        "DynamoDB.py",
        "EC2Instance.py",
        "DiskVolumes.py",
        "Lambda.py",
        "SecurityGroups.py",
        "OrphanedSnapshotsVolumesAMIs.py",
        "s3repl_latest.py",
        "AWSCosting.py",
        "KMS_Cost_with_StorageLens_S3.py",
    ]

    selected_files = reports(file_names)
    output_folder = create_output_folder()

    aws_profile = input("Enter AWS profile: ").strip()
    aws_region = input("Enter AWS region (or 'all' for all regions): ").strip()

    with multiprocessing.Pool(processes=6) as pool:
        partial_run = functools.partial(run_python_file, output_folder=output_folder, aws_profile=aws_profile, aws_region=aws_region)
        pool.map(partial_run, selected_files)
    
    print("Selected files executed.")

    move_report_files(output_folder)
    print(f"Reports moved to {output_folder}.")

if __name__ == "__main__":
    main()