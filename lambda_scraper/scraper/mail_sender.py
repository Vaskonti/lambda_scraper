import boto3
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
ses_client = boto3.client('ses')

def load_html_file(file_path):
    return env.get_template(file_path)


def send_email(subject, body, receivers):
    ses_client.send_email(
        Destination={
            'ToAddresses': receivers,
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': "UTF-8",
                    'Data': body,
                },
            },
            'Subject': {
                'Charset': "UTF-8",
                'Data': subject,
            },
        },
        Source=os.environ['EMAIL_SENDER'],
        SourceArn=os.environ['EMAIL_SENDER_ARN'],
    )
