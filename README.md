# awspythonreports
#### Video Demo:  <URL HERE>
#### Description:

This is a collection of Python scripts and is designed to interact with various Amazon Web Services (AWS) components. Each script serves a specific purpose, from managing AWS resources to extracting and analyzing AWS-related data. There are 14 scripts and each refer to a specific AWs service and reports on it. There is a detailed description on what each script does, their dependencies and requirements have been added for each script. The master script called "project.py" allows the end user to run all the scripts for all AWS services or just for few AWS services and report on them. 

PROJECT.PY:

The Python script project.py is a multifaceted utility involving multiple aspects of system and process management. It uses modules like multiprocessing, importlib, os, and subprocess, indicating functionalities related to parallel processing, dynamic module loading, file system operations, and running external commands. The script includes functions for running AWS CLI commands and executing Python files, hinting at its potential use in automated workflows or cloud management tasks.

Overview: project.py is a versatile Python script designed to facilitate automated workflows and cloud management tasks. It leverages various Python modules to handle parallel processing, dynamic module loading, file system interactions, and execution of external commands. This script is particularly useful for AWS cloud management, including running AWS CLI commands and executing Python files in different environments.

Features:
    AWS CLI Command Execution: Executes AWS CLI commands and captures their output, which is useful for automating AWS cloud management tasks.
    Python File Execution: Provides functionality to run Python files, potentially with AWS account-specific configurations.
    Multiprocessing Support: Utilizes the multiprocessing module for parallel execution of tasks, enhancing efficiency.
    Dynamic Module Importing: Dynamically imports modules, allowing for flexible script execution based on runtime requirements.
Prerequisites:
    Python 3.x
    AWS CLI installed and configured (for AWS-related tasks)
    Access to the necessary AWS account and permissions (if interacting with AWS services)
    Setup and Configuration
    Ensure your system has Python 3.x installed and configured. For AWS-related functionalities, AWS CLI must be installed and properly set up with your AWS credentials.

Usage: 
The script is executed from the command line as follows: python project.py
Depending on the script's functionalities and your specific use case, additional arguments or environmental setup may be required.

Functionality Details:
    AWS CLI Command Execution: This function runs specified AWS CLI commands. It captures and returns the output, handling any errors encountered during execution.
    Python File Execution: Allows for running Python files within the script. Can be configured to pass AWS account-specific information or other parameters.
    Multiprocessing and Dynamic Importing: The script can perform tasks in parallel, utilizing Python's multiprocessing capabilities.
    It can dynamically import modules as required, adding flexibility to its operation. 

Services and scripts called in the project.py:

    S3.py
    Aurora.py
    RDS.py
    Redshift.py
    NATGateway.py
    DynamoDB.py
    EC2Instance.py
    DiskVolumes.py
    Lambda.py
    SecurityGroups.py
    OrphanedSnapshotsVolumesAMIs.py
    s3repl_latest.py
    AWSCosting.py
    KMS_Cost_with_StorageLens_S3.py

Customization:
The script can be tailored to include more specific AWS tasks, handle different types of subprocesses, or work with other cloud providers. Additional error handling, logging, or reporting features can be integrated.

Below is a bit detailed description of all the services and scripts which are part of this module.

1. Aurora.py
Purpose: Handles AWS Aurora database information.

Imports: boto3, pandas
Main Functions:
    get_aurora_database_info: Retrieves information about Aurora databases.
    main: Main function to execute the script.
Description: The script appears to fetch information from AWS Aurora databases and may write this data to an Excel file using pandas.

2. AWSCosting.py
Purpose: Manages AWS Cost Explorer data.

Imports: boto3, datetime, pandas
Main Functions:
    get_cost_data: Retrieves cost data from AWS Cost Explorer.
    save_to_excel: Saves the retrieved data to an Excel file.
    main: Main function to run the script.
Description: This script sets up a Boto3 client for the AWS Cost Explorer service to fetch and manage AWS cost data.

3. DiskVolumes.py
Purpose: Manages disk volumes in AWS.

Imports: boto3, csv
Main Functions:
    main: Main function to run the script.
Description: The script focuses on initializing a Boto3 session, likely for operations related to AWS disk volumes such as EBS, ephemeral EC2 instance store.

4. DynamoDB.py
Purpose: Interacts with AWS DynamoDB.

Imports: boto3, pandas, openpyxl
Main Functions:
    main: Main function to run the script.
Description: This script is designed to initialize a Boto3 DynamoDB client, probably for operations involving DynamoDB data.This scripts reports on the variopus attributes of DynamoDB such as RCUs, WCU and amount of data in DynamoDB tables.


5. EC2Instance.py 
Purpose: EC2Instance.py is a Python script designed for managing AWS EC2 instances. It utilizes the boto3 library to interact with AWS services, providing functionalities to describe regions and manage EC2 instance inventories.

Features
Session Initialization: Configures a session with AWS using specified credentials.
Region Description: Retrieves a list of all available AWS regions.
EC2 Inventory Management: Generates a CSV file listing details of EC2 instances across all regions.
Prerequisites: Python 3.x, boto3 library (pip install boto3), AWS account with configured access and secret keys. Before running the script, ensure you have set up your AWS credentials. The script uses a profile named "elonmusk". Replace it with your AWS profile name.
The generated CSV file includes the following columns:
    Serial Number
    Instance ID
    Image ID
    Instance Lifecycle
    (additional columns based on the script's output)

6. KMS_Cast_with_StorageLens_S3.py

Overview: KMS_Cost_with_StorageLens_S3.py is a Python script for managing and analyzing AWS S3 buckets. It leverages the boto3 SDK to perform various operations related to S3 buckets and integrates with AWS's Storage Lens for advanced storage insights.

Features:
    Bucket Object Count: Retrieves the number of objects in specified S3 buckets.
    List All Buckets: Lists all S3 buckets in the AWS account.
    Identify Read-Heavy Buckets: Uses AWS Storage Lens to identify buckets with high read operations.
Prerequisites: Python 3.x, boto3 library (pip install boto3), pandas library (pip install pandas), An AWS account with configured S3 and KMS services, Access to AWS Storage Lens

7. Lambda.py

Overview: Lambda.py is a Python script tailored for managing and analyzing AWS Lambda functions. It utilizes the boto3 SDK to interact with Lambda services, offering functionalities such as listing Lambda functions and analyzing their configurations across multiple AWS regions.

Features: 
    Listing Lambda Functions: Retrieves a list of Lambda functions available in the AWS account across all regions.
    Regional Analysis: Allows analysis of Lambda functions in different AWS regions.
Prerequisites: Python 3.x, boto3 library (pip install boto3), pandas library (pip install pandas), An active AWS account with access to AWS Lambda, Ensure your AWS credentials are correctly configured for access to Lambda services. The script employs the default credential configuration of boto3.

8. NATGateway.py

Overview: NATGateway.py is a Python utility script for managing and analyzing AWS NAT Gateways. It leverages the boto3 SDK to interact with AWS services, primarily focusing on operations related to NAT Gateways in multiple AWS regions.

Features:
    Listing NAT Gateways: Retrieves and lists NAT Gateways available across all AWS regions.
    Regional Analysis: Allows for the analysis of NAT Gateway configurations and metrics in different regions.
Prerequisites: Python 3.x, boto3 library (pip install boto3), pandas library (pip install pandas), An AWS account with appropriate permissions to access NAT Gateway information.
Setup and Configuration: Before running the script, ensure your AWS credentials are set up correctly. The script uses a profile named "elonmusk"; replace this with your AWS profile name.

Depending on the script's implementation, the output may include NAT Gateway IDs, statuses, metrics, and other relevant information. This could be displayed in the console, saved to a file, or exported to a CSV format.

9. OrphanedSnapshotsVolumesAMIs.py

Overview: OrphanedSnapshotsVolumesAMIs.py is a Python script aimed at identifying and managing orphaned AWS resources, including snapshots, volumes, and AMIs. The script uses the boto3 SDK for interactions with AWS services, providing an efficient way to audit and clean up unused or unattached resources.

Features:
    Identifying Orphaned Snapshots: Locates snapshots that are no longer in use.
    Finding Unattached Volumes: Identifies volumes that are not attached to any EC2 instances.
    Detecting Unused AMIs: Lists AMIs that are not associated with any running or stopped instances.
Prerequisites: Python 3.x, boto3 library (pip install boto3), pandas library (pip install pandas), An AWS account with necessary permissions to access EC2, Snapshots, and AMI information

The script will provide a list of orphaned snapshots, unattached volumes, and unused AMIs across the specified AWS regions.
The output may include detailed information about each resource type, including IDs, creation dates, and attachment status. This information might be printed to the console, saved in a file, or exported in CSV format.

10. RDS.py

Overview: RDS.py is a Python script designed for managing and analyzing AWS Relational Database Service (RDS) instances. It utilizes the boto3 SDK to interact with AWS services, offering functionalities such as listing RDS instances, extracting their configuration details, and providing insights into their usage across multiple AWS regions.

Features: 
    Listing RDS Instances: Retrieves a list of RDS instances available in the AWS account across all regions.
    Database Configuration Analysis: Gathers detailed information on the configuration of each RDS instance, including database engine, size, and security settings.
    Regional Analysis: Allows for an analysis of RDS instances in different AWS regions.
Prerequisites: Python 3.x, boto3 library (pip install boto3), pandas library (pip install pandas), An AWS account with appropriate permissions for RDS access. Before running the script, ensure your AWS credentials are correctly configured. The script uses a profile named "elonmusk"; replace this with your AWS profile name.

The output may include RDS instance names, availability zones, regions, VPCs, security groups, database engines, sizes, and other relevant information. This could be displayed in the console, saved to a file, or exported in CSV format.

11. Redshift.py

Overview: Redshift.py is a Python script designed for managing and analyzing Amazon Redshift clusters. It leverages the boto3 SDK to interact with AWS services, focusing on operations related to Amazon Redshift in multiple AWS regions.

Features
    Listing Redshift Clusters: Retrieves and lists Redshift clusters available across all AWS regions.
    Cluster Configuration Analysis: Gathers detailed information on the configuration of each Redshift cluster, including size, security settings, and snapshots.
    Regional Analysis: Allows for an analysis of Redshift clusters in different AWS regions.
Prerequisites: Python 3.x, boto3 library (pip install boto3), pandas library (pip install pandas), An AWS account with appropriate permissions for Redshift access, Ensure your AWS credentials are correctly configured. The script uses a profile named "elonmusk"; replace this with your AWS profile name.
The output may include Redshift cluster names, availability zones, regions, VPCs, security groups, sizes, utilized sizes, snapshot settings, and other relevant information. This could be displayed in the console, saved to a file, or exported in CSV format.

12. S3.py

Overview: S3.py is a Python script designed for managing and analyzing Amazon S3 buckets. It utilizes the boto3 SDK for interactions with AWS services, focusing on operations related to S3 buckets such as retrieving their details, analyzing configurations, and assessing security settings.

Features:
    Listing S3 Buckets: Retrieves a list of S3 buckets and their key details.
    Bucket Configuration Analysis: Gathers information on bucket configurations, including size, versioning status, encryption status, storage class, and more.
    Security and Efficiency Assessment: Evaluates buckets for security features like encryption and object lock, as well as storage efficiency through settings like intelligent tiering.
Prerequisites: Python 3.x, boto3 library (pip install boto3), pandas library (pip install pandas), An AWS account with the necessary permissions to access S3 bucket information. 

The output may include details such as bucket names, regions, sizes, versioning status, encryption status, and other relevant information, displayed in the console, saved in a file, or exported in CSV format.

13. s3repl_latest.py

Overview: s3repl_latest.py is a Python script dedicated to managing and analyzing Amazon S3 replication configurations. It uses the boto3 SDK to interact with AWS services, focusing on operations related to replication rules and settings across S3 buckets.

Features:
    Listing S3 Buckets: Retrieves a list of all S3 buckets in the AWS account.
    Replication Rule Retrieval: Gathers replication rules set for each S3 bucket.
    Replication Configuration Analysis: Analyzes the replication configurations for efficiency and compliance with best practices.
Prerequisites: Python 3.x, boto3 library (pip install boto3), pandas library (pip install pandas), openpyxl library (pip install openpyxl), An AWS account with appropriate permissions to access S3 bucket replication settings.
Enter the AWS account ID when prompted. The script will then process and output replication configuration details for S3 buckets.
The output includes details about each bucket's replication rules and configurations. This information might be printed to the console, saved in a file, or exported in an Excel format using openpyxl.

14. SecurityGroups.py

Overview: SecurityGroups.py is a Python script designed for managing and analyzing AWS Security Groups. It uses the boto3 SDK to interact with AWS services, focusing on operations related to security groups such as retrieving their configurations and assessing their security rules across different AWS regions.

Features
    Listing Security Groups: Retrieves a list of all security groups across all AWS regions.
    Security Group Configuration Analysis: Analyzes the configurations and rules of each security group for potential security risks or inefficiencies.
    Multi-Regional Analysis: Allows for a comprehensive analysis of security groups in various AWS regions.
Prerequisites: Python 3.x, boto3 library (pip install boto3), pandas library (pip install pandas), An AWS account with appropriate permissions for accessing security group information. The output may include details such as security group IDs, names, inbound and outbound rules, and other relevant information, displayed in the console, saved in a file, or exported in CSV format.

test_project.py

Overview: test_project.py is a test suite written in Python, designed to test functionalities of a Python script (presumably project.py). It employs the unittest framework and uses mock objects to simulate the behavior of real objects in the script, allowing for an isolated and controlled testing environment.

Features:
    Unit Testing: Implements unit tests to validate individual units of code in the associated Python script.
    Mocking Dependencies: Uses mock objects to simulate the behavior of complex or external dependencies, like AWS CLI commands.
    Patch Mechanism: Employs the patch mechanism to temporarily replace real objects with mock objects during test execution.
    Integration with project.py: Specifically designed to test the project.py script, ensuring its functions behave as expected.
Prerequisites: Python 3.x, unittest module (included in standard Python library), project.py script (or the script this test suite is designed to test). 

Test Suite Details: 
    Mocking External Calls: Mocks external calls, such as AWS CLI commands, to avoid interacting with real-world systems during testing.
    Ensures that tests remain fast and reliable.
    Testing Various Scenarios: Includes tests for different scenarios and edge cases to ensure comprehensive coverage of the script's functionalities.
    Assertion of Results: Asserts the expected outcomes from the script's functions, validating their correctness and stability.