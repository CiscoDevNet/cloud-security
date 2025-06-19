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

''' Get summary information from Network Tunnels to detect Tunnels in "Disconnected" or "Warning" state '''


# Export/Set the environment variables
from SSEAPI import SSEAPI
from email.message import EmailMessage
import smtplib
import datetime
import os
client_id = os.environ.get('API_KEY')
client_secret = os.environ.get('API_SECRET')
email_address = os.environ.get('EMAIL')
passw = os.environ.get('PASSWD')
recipients = ['REPLACE_THIS_VALUE_WITH_YOUR_EMAIL_ADDRESS']
token_url = os.environ.get(
    'TOKEN_URL') or 'https://api.sse.cisco.com/auth/v2/token'

def send_email(tunnelInfo):
    """This function will send an alert to the desired recipients"""
    msg = EmailMessage()
    msg['Subject'] = 'Network Tunnel Error Found!'
    msg['From'] = email_address
    msg['To'] = recipients
    msg.set_content(
        f'Connection Error found in Network Tunnel(s). With status DISCONNECTED. Please check your SSE Dashboard for more information')

    msg.add_alternative("""
    <!DOCTYPE >
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Network Tunnel Monitor</title>
    </head>
    <body>
        <h1>Tunnel connection error detected at """ + str(datetime.datetime.now()) + """</h1>
        <p>The Tunnel Monitor script detected a connection error with: """ + tunnelInfo +"""</p>
        <br/>
        <p>Please check your SSE dashboard.</p>

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
        sse_api = SSEAPI(token_url, client_id, client_secret)

        # Step 2: Send a request checking for status of the Tunnel Groups
        tunnel_endpoints = 'deployments/v2/networktunnelgroups'
        tunnelComponents = sse_api.ReqGet(tunnel_endpoints).json()
        tunnelData = tunnelComponents["data"]
        tunnelInfo ="<ul>"
        for i in tunnelData:
            if i["status"] == "disconnected" or i["status"] == "warning":
                tunnelInfo = tunnelInfo + "<li>" + i["name"] + " " + i["deviceType"] + " " + i["status"] + "</li>"
        tunnelInfo = tunnelInfo + "</ul>"
        send_email(tunnelInfo)

    except Exception as e:
        raise (e)