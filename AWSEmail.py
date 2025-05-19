import boto3 # pip install boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os
# Create a new SES resource and specify a region.

def email_notify(RECIP, subject, body):


    SENDER = "AWS SES Email Support <email@domain.com>"
    #print(RECIP)
    recipients = RECIP
    #recipients = ["email1@domain.com","email2@domain.com"]
    print(recipients)
    RECIPIENT = ','.join(recipients)
    # If necessary, replace us-east-1 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"
    #The subject line for the email.
    SUBJECT = subject
    BODY_TEXT = body
    # The character encoding for the email.
    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION)

    # Create a multipart/mixed parent container.
    msg = MIMEMultipart('mixed')
    # Add subject, from and to lines.
    msg['Subject'] = SUBJECT 
    msg['From'] = SENDER 
    msg['To'] = RECIPIENT
    msg['reply-to'] = 'email.domain.com'
    # Create a multipart/alternative child container.
    #msg_body = MIMEMultipart('alternative')
    # Encode the text and HTML content and set the character encoding. This step is
    # necessary if you're sending a message with characters outside the ASCII range.
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    #htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
    # Define the attachment part and encode it using MIMEApplication.
    #att = MIMEBase('application', "octet-stream")
    #att.set_payload(open(attach, "rb").read())
    #encoders.encode_base64(att)
    # Add a header to tell the email client to treat this part as an attachment,
    # and to give the attachment a name.
    #att.add_header('Content-Disposition','attachment',filename=os.path.basename(attach))
    

    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(textpart)

    # Add the attachment to the parent container.
    #msg.attach(att)
    #print(msg)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        print(msg.as_string())
        print("********************************")
        print(RECIPIENT)
        response = client.send_email(
        #response = client.send_email(
            Source=SENDER,
            Destination={
                'ToAddresses': recipients
                },
        #    RawMessage={
        #         'Data':msg.as_string(),
        #     },
            Message={
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': body,
                    },
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': body,
                    },
                    },
                    'Subject': {
                        'Charset': 'UTF-8',
                        'Data': subject,
                    },
            },
            ReplyToAddresses=[
                'email@domain.com'
                ],

            SourceArn='from AWS SES ',
            ReturnPathArn='from AWS SES '
            #ConfigurationSetName=CONFIGURATION_SET
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response)




# Top-level script environment invocation allows for script to be more portable
if __name__ == '__main__':
    email_notify(["email@domain.com"],"test", "test<br>  test\n <a href='https://aws.amazon.com/'>AWS Home</a>")