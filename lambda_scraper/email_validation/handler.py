import json
import boto3
import os

ses = boto3.client('ses')
lambda_client = boto3.client('lambda')


def handler(event, context):
    email = event.get('email')
    # Verify the email identity with AWS SES
    response = ses.verify_email_identity(EmailAddress=email)
    print(f"Verification initiated for {email}")

    # Update the environment variable of the third Lambda function
    function_name = os.environ['SCRAPER_ARN']

    # Get the current environment variables of the third Lambda function
    response = lambda_client.get_function_configuration(FunctionName=function_name)
    current_env_vars = {'RECEIVERS': ''}
    if response['Environment'] is not None and 'Variables' in response['Environment']:
        current_env_vars = response['Environment']['Variables']

    current_env_vars['RECEIVERS'] = current_env_vars['RECEIVERS'] + ',' + email
    lambda_client.update_function_configuration(
        FunctionName=function_name,
        Environment={
            'Variables': current_env_vars
        }
    )
    print(f"Updated environment variable for {function_name} with email {email}")

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'message': 'Email verification initiated and environment variable updated'})
    }
