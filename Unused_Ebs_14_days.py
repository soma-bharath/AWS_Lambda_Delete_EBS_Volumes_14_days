import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Get all EBS volumes
    response = ec2.describe_volumes()

    # Get current time
    current_time = datetime.utcnow()

    # Iterate through volumes
    for volume in response['Volumes']:
        # Check for attachment information
        if 'Attachments' in volume:
            # Get the attachment information
            attachment_info = volume['Attachments'][0]

            # Calculate the difference in days between current time and attachment time
            attach_time = attachment_info['AttachTime']
            days_difference = (current_time - attach_time).days
            #minutes_difference = (current_time - attach_time).total_seconds() / 60

            # If the volume is not in use for more than 14 days, delete it
            if days_difference > 14:
                print(f"Deleting EBS volume {volume['VolumeId']} which has been unused for {days_difference} days.")
                ec2.delete_volume(VolumeId=volume['VolumeId'])
        else:
            # If the volume is not attached, it's not in use
            print(f"Deleting EBS volume {volume['VolumeId']} which is not attached.")
            ec2.delete_volume(VolumeId=volume['VolumeId'])

    return {
        'statusCode': 200,
        'body': 'EBS volumes cleanup completed.'
    }
