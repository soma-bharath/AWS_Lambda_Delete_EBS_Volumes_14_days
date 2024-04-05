import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Get all instances
    instances = ec2.describe_instances()

    # Iterate through instances
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_state = instance['State']['Name']

            # Check if instance is running or stopped
            if instance_state == 'running':
                ec2.stop_instances(InstanceIds=[instance_id])
                print(f"Instance {instance_id} stopped.")
            elif instance_state == 'stopped':
                print(f"Instance {instance_id} is in stop state already.")
            else:
                print(f"Instance {instance_id} is in {instance_state} state. Skipping.")

    return {
        'statusCode': 200,
        'body': 'EC2 instances scheduled start and stop completed.'
    }
