import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    instance_id = 'your-instance-id'
    image_description = 'Automated backup'
    image_name = f'Backup-{instance_id}-{event["time"]}'

    response = ec2.create_image(InstanceId=instance_id, Name=image_name, Description=image_description, NoReboot=True)
    print(response)
