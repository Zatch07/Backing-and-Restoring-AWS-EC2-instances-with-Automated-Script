# Backing and Restoring AWS EC2 instances with Automated Script
 backing up an aws instances for rollback every 7 days and restoring it to the backed-up state.


## Setting Up an AWS Account

1. **Create an AWS Account**:
   - Visit the [AWS homepage](https://aws.amazon.com/) and sign up.
   - You'll need to provide basic information and a valid credit card.
   - You'll get a free account for 1 year with limited functionality.

2. **Access the AWS Management Console**:
   - Once your account is set up, log in to the [AWS Management Console](https://aws.amazon.com/console/).
   - This is your central hub for managing AWS services.

### Creating an EC2 Instance in AWS

#### 1: Launch Instance

1. Inside the EC2 Dashboard, click on the **Launch Instance** button. This starts the process of creating a new EC2 instance.

### 2: Choose an Amazon Machine Image (AMI)

1. You will be presented with a list of Amazon Machine Images (AMIs). Select the AMI that suits your requirements. 
   - For beginners, Amazon Linux 2 AMI or Ubuntu Server are popular choices.

### 3: Choose an Instance Type

1. Select the instance type you require. 
   - For testing purposes or small workloads, a "t2.micro" instance is a good start as it is eligible for the AWS Free Tier.
2. Click on **Next: Configure Instance Details**.

### 4: Configure Instance

1. Configure the instance details according to your needs. This includes settings like network, subnet, IAM roles, and more. 
   - For a basic setup, you can leave the default settings.
2. Proceed to **Next: Add Storage**.

### 5: Add Storage

1. Modify the storage settings if necessary. The default allocation is usually sufficient for basic applications.
2. Click on **Next: Add Tags**.

### 6: Add Tags

1. Optionally, add tags to your instance. Tags are key-value pairs that help you manage, identify, organize, search for, and filter resources.
2. Proceed to **Next: Configure Security Group**.

### 7: Configure Security Group

1. A security group acts as a virtual firewall. You can either select an existing security group or create a new one.
   - For a new security group, ensure you allow SSH access (port 22) at a minimum. For a web server, also allow HTTP (port 80) and HTTPS (port 443).
2. Click on **Review and Launch**.

### 8: Review and Launch

1. Review your instance configuration. Make any necessary adjustments by going back to the previous steps.
2. Click **Launch**.
3. You will be prompted to select a key pair. Use an existing key pair or create a new one. If creating a new one, download and save it securely; you will need it to SSH into your instance.
4. After selecting your key pair, acknowledge that you have access to the selected private key file by checking the box.
5. Click **Launch Instances**.

## Connecting to an EC2 Instance Using VS Code

### Step 1: Install the Remote - SSH Extension

1. Open VS Code.
2. Go to the Extensions view by clicking on the square icon on the sidebar or pressing `Ctrl+Shift+X`.
3. Search for `Remote - SSH` and click on the install button.

### Step 2: Configure SSH

1. Before connecting, ensure your private key file permissions are correctly set. On Linux and Mac, you can set the permissions by running `chmod 400 /path/to/your-key.pem` in your terminal.
2. Open VS Code Command Palette by pressing `Ctrl+Shift+P` or `Cmd+Shift+P` on Mac.
3. Type `Remote-SSH: Open Configuration File` and select it.
4. Choose the configuration file to edit. If unsure, select `config` in your SSH folder.
5. Add a new entry for your EC2 instance in the configuration file. Replace `your-instance-user`, `your-instance-ip`, and `/path/to/your-key.pem` with your instance's SSH username (like `ec2-user` for Amazon Linux AMI which I used), IP address, and the path to your private key file, respectively.

    ```ssh
    Host my-ec2-instance
        HostName your-instance-ip
        User your-instance-user
        IdentityFile /path/to/your-key.pem
    ```

6. Save and close the configuration file.

### Step 3: Connect to Your EC2 Instance

1. Press `Ctrl+Shift+P` or `Cmd+Shift+P` on Mac to open the Command Palette again.
2. Type `Remote-SSH: Connect to Host...` and select it.
3. Choose `my-ec2-instance` from the list (or the host name you configured).
4. A new VS Code window will open, and you'll be connected to your EC2 instance. It might take a moment for the connection to establish and for VS Code to set up the remote environment.

## Adding a Random File to Your EC2 Instance via VS Code

### Step 1: Creating a Ramdom file
1. Use the command. This will create a randomfile.txt with a size of 1MB.
    ```bash
    dd if=/dev/urandom of=randomfile.txt bs=1M count=1

### Step 2: Verify the File on the EC2 Instance (Optional)

To ensure that the file has been added to your EC2 instance, you can verify it directly through the terminal in VS Code.

1. Use the `ls` command to list the files in the current directory.

    ```bash
    ls -l

## Granting IAM Permissions to Create an AMI

To create an Amazon Machine Image (AMI), your IAM user or role needs specific permissions. Follow these steps to grant the necessary permissions.


### Step 1: Navigate to IAM Dashboard

1. Once logged in, find and click on **Services** at the top of the page.
2. Under the **Security, Identity, & Compliance** section, click on **IAM** to open the IAM dashboard.

### Step 2: Identify the IAM User or Role

1. In the IAM dashboard, click on **Users** if you're assigning permissions to a user. If you're assigning permissions to a role (for instance, for an EC2 instance or a Lambda function), click on **Roles** instead.
2. Find and click on the user or role you want to grant permissions to.

### Step 3: Attach the Policy for AMI Creation

1. On the user or role detail page, click on the **Permissions** tab.
2. Click on **Add permissions** button.
3. Choose **Attach existing policies directly**.
4. Search for `AmazonEC2FullAccess` policy. This policy allows for full access to EC2 resources, including the ability to create AMIs.

### Step 4: Verify the Permissions
1. Ensure the policy is attached by reviewing the Permissions tab for the user or role.
2. The user or role should now have the necessary permissions to create an AMI.


## Manually Creating an AMI

### Step 1: Open the Integrated Terminal in VS Code

- With your SSH session active in VS Code, open the integrated terminal by selecting **Terminal > New Terminal** from the main menu or using the `Ctrl+`` shortcut.

### Step 2: Install AWS CLI (if necessary)

If AWS CLI is not installed on your EC2 instance, install it by running:
    ```bash
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install

### Step 3: Configure AWS CLI
- If not already configured, set up the AWS CLI with your credentials:
    ```bash
    aws configure

- Enter your AWS Access Key ID, Secret Access Key, region, and output format as prompted.
    
### Step 4: Create the AMI
- Run the following command to create an AMI from your instance. Replace 'instance-id' with your actual instance ID and 'MyAMIName' with your desired AMI name.
    
    ```bash
    aws ec2 create-image --instance-id instance-id --name "MyAMIName" --description "An AMI of my instance" --no-reboot

- '--no-reboot' is optional and ensures the instance isn't rebooted during the AMI creation process. Omit this if you prefer the instance to reboot for a clean state.


## Automating AMI Creation Every 7 Days

Automating the AMI creation process requires using AWS Lambda and Amazon EventBridge (formerly CloudWatch Events).

### Create an IAM Role for AWS Lambda

#### 1. Create IAM Role

- Navigate to the IAM Dashboard, select **Roles**, and click **Create role**.
- Choose **AWS service** as the trusted entity and select **Lambda** as the use case.
- Attach the `AmazonEC2FullAccess` policy and any other necessary permissions, then proceed to create the role.

### Create a Lambda Function

#### 1. Navigate to AWS Lambda

- Go to the AWS Lambda console and click **Create function**.

#### 2. Configure the Function

- Choose **Author from scratch**.
- Name your function and select the IAM role you created earlier.
- Choose Python or another preferred runtime.

#### 3. Function Code
- Use the code in [Lambda.py](https://github.com/Zatch07/Backing-and-Restoring-AWS-EC2-instances-with-Automated-Script/blob/main/lambda.py)
- Replace 'your-instance-id' with your actual instance ID.

#### 4. Save the Lambda Function

- After entering your code in the AWS Lambda console, click **Save** to preserve your function.

### Schedule the Lambda Function with Amazon EventBridge

#### Create a Rule:

1. Navigate to the **Amazon EventBridge console** and click **Create rule**.
2. Provide a meaningful **rule name** and **description**.

#### Schedule:

1. For the rule type, select **Schedule**.
2. Enter a cron expression to specify the trigger schedule. To run the function at midnight UTC every 7 days, use: `cron(0 0 */7 * ? *)`.

#### Select Target:

1. Under **Select target**, choose **Lambda function**.
2. Select the Lambda function you wish to trigger.

#### Configure Input:

1. Choose **Constant (JSON text)** if you need to pass specific data to your Lambda function upon execution.
2. Provide the necessary JSON text that your Lambda function expects.

#### Create the Rule:

1. Review your rule settings to ensure everything is configured as desired.
2. Click **Create rule** to finalize and activate the scheduled execution of your Lambda function.

By following these steps, you've successfully scheduled your Lambda function to run automatically every 7 days using Amazon EventBridge, enabling regular task execution without manual intervention.


## Restoring an AMI to a New EC2 Instance and Verifying File Presence

This guide will walk you through the process of launching a new EC2 instance from an Amazon Machine Image (AMI) and verifying that a specific file (`randomfile.txt`) exists on the new instance.

### Step 1: Launch a New Instance from the AMI

1. **Log in to the AWS Management Console**:
   - Navigate to the [AWS Management Console](https://aws.amazon.com/console/) and sign in.

2. **Access the EC2 Dashboard**:
   - Find and select **EC2** from the Services menu to open the EC2 Dashboard.

3. **Launch a New Instance**:
   - Click on the **Launch Instances** button.
   - In the **Choose an Amazon Machine Image (AMI)** section, select **My AMIs** on the left side. This will display the AMIs you have created.
   - Find the AMI you want to use for restoration and click on the **Select** button next to it.

4. **Choose an Instance Type**:
   - Select the instance type you wish to use. You can choose the same type as the original instance or a different one depending on your requirements.
   - Click **Next: Configure Instance Details**.

5. **Configure Instance and Add Storage** (optional):
   - Configure the instance details as needed. The default options are typically sufficient.
   - Click **Next** until you reach the **Configure Security Group** section.

6. **Configure Security Group**:
   - You can select an existing security group or create a new one. Ensure that the security group allows you access to connect to the instance, typically through SSH (port 22).
   - Click **Review and Launch**.

7. **Review and Launch**:
   - Review your instance settings. If everything is correct, click **Launch**.
   - You will be prompted to select a key pair. Use an existing key pair or create a new one, then click **Launch Instances**.

### Step 2: Connect to the New EC2 Instance

1. **Wait for the Instance to Initialize**:
   - It may take a few minutes for your instance to launch and pass status checks.

2. **Connect to Your Instance**:
   - Once the instance is running, select it in the EC2 Dashboard and click on the **Connect** button.
   - Follow the provided instructions to connect to your instance using your chosen method (SSH for Linux/macOS, RDP for Windows instances).

### Step 3: Verify the File Exists

Once connected to your instance:

1. **Check for the File**:
   - Use the `ls` command to list the contents of the directory where `randomfile.txt` should exist. For example:

    ```bash
    ls /path/to/directory

