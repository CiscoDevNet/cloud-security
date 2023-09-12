"""
Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

''' Get summary information from VAs to detect AD Connectors in error state '''


# Export/Set the environment variables
from UmbrellaAPI import UmbrellaAPI
from email.message import EmailMessage
import smtplib
import datetime
import os
client_id = os.environ.get('API_KEY')
client_secret = os.environ.get('API_SECRET')
email_address = os.environ.get('EMAIL_ADDRESS')
passw = os.environ.get('PASSWD')
recipients = os.environ.get('RECIPIENTS')
token_url = os.environ.get(
    'TOKEN_URL') or 'https://api.umbrella.com/auth/v2/token'

def send_email(component):
    """This function will send an alert to the desired recipients"""
    msg = EmailMessage()
    msg['Subject'] = 'AD Connector Error Found!'
    msg['From'] = email_address
    msg['To'] = recipients
    msg.set_content(
        f'Connection Error found in {component}. Please check your Umbrella Dashboard and connectivity to all DCs')

    msg.add_alternative("""
    <!DOCTYPE >
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AD Connector Monitor</title>
    </head>
    <body>
        <h1>AD Connector Error Detected at """ + str(datetime.datetime.now()) + """</h1>
        <p>The AD Connector Monitor script detected an error with: """ + component + """.</p>
        <br/>
        <p>Please check your Umbrella dashboard.</p>

        <style type="text/css">
            body{
                margin: 0;
                background-color: #cccccc;
            }
        </style>
        
    </body>
    </html>
    """, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, passw)
        print('login success')
        smtp.send_message(msg)
        print("Email has been sent to: ", recipients)


# main
if __name__ == '__main__':

    # Exit out if the required API_KEY and API_SECRET are not set in the environment
    for var in ['API_SECRET', 'API_KEY']:
        if os.environ.get(var) == None:
            print("Required environment variable: {} not set".format(var))
            exit()

    try:
        # Step 1: Create the API client
        umbrella_api = UmbrellaAPI(token_url, client_id, client_secret)

        # Step 2: Send a request checking for status of the AD Connector
        umbrella_AD_endpoint = 'deployments/v2/virtualappliances'
        adComponents = umbrella_api.ReqGet(umbrella_AD_endpoint).json()

        # Step 3: Check the status of the components, call send_email() if error is found in a component
        for component in adComponents:
            if (component.get("type") == "connector" and component.get("health") == "error"):
                send_email(component.get("name"))

    except Exception as e:
        raise (e)