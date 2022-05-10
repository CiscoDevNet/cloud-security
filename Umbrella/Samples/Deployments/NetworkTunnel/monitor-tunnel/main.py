#!/usr/bin/env python3

"""
Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at "https://developer.cisco.com/docs/licenses"
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS IS"
BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

----------------------------------------------------------------------
"""

import requests
from smtplib import SMTP_SSL as SMTP
from smtplib import SMTPException
from email.mime.text import MIMEText
from datetime import datetime
import json, time

''' Get Network Tunnel State and write response to log file '''
def get_tunnel_states(key, secret, org_id, max_inactive_interval):
    logfile.write("GET /tunnelsState\n")
    response = requests.get(
        url="https://management.api.umbrella.com/v1/organizations/{organizationId}/tunnelsState".format(organizationId=org_id),
        headers={
            'accept': 'application/json',
            'content-yype': 'application/json'
        },
        auth=(key, secret))
    logfile.write("Response: Status = {}, Message Content = {}\n".format(response.status_code, response.text))

    # Report error if response is not 200/OK
    if not response.ok:
        #response.raise_for_status()
        logfile.write("ERROR: Response Status is not 200/OK \n")
        return (json.loads(f'{{"update status": "Script fail", "reason": "ERROR: API Request fail, status = {response.status_code}" }}'))

    # Check Network Tunnel State
    tmp = []
    for tunnel in response.json():
        tunnel_id = tunnel.get("tunnelId")
        logfile.write("Checking Tunnel state for {}.\n".format(tunnel_id))

        if tunnel.get("status") != "UP":
            logfile.write("Tunnel {} state is {}.\n".format(tunnel_id, tunnel.get("status")))
            #Tunnel state is not UP
            tunnel["monitor_result"] = tunnel.get("status")
            tmp.append(tunnel)
        else:
            #Tunnel state is UP, check it with last status
            last_modified_timestamp = datetime.strptime( tunnel.get("modifiedAt")[:-4], "%Y-%m-%dT%H:%M:%S.%f")
            delta_since_last_update = (datetime.utcnow()-last_modified_timestamp).total_seconds()
            logfile.write("Tunnel {} last state update {} seconds ago.  ".format(tunnel_id, delta_since_last_update))

            #if last 'modifiedAt' time delta is greater than configured MAX_INACTIVE_INTERVAL, then the tunnel is INACTIVE
            if delta_since_last_update > max_inactive_interval:
                logfile.write("Tunnel is UP but INACTIVE.\n")
                tunnel["monitor_result"] = "UP_BUT_INACTIVE"
                tmp.append(tunnel)
            else:
                logfile.write( "Tunnel UP {} and ACTIVE {}.\n".format(tunnel_id, delta_since_last_update))

    return tmp

''' Send email notification about state of Network Tunnels '''
def send_email(server, sender, receiver, subject, content, username="", password="", sub_type="plain"):
    text_subtype = sub_type
    content = json.dumps(content, indent=4, sort_keys=True)
    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender # some SMTP servers automatically set up the From field, but not all

        logfile.write("Try connection to mail server.\n")
        conn = SMTP(server)
        conn.set_debuglevel(False)
        conn.login(username, password)
        try:
            conn.sendmail(sender, [receiver], msg.as_string())
        except Exception as e:
            logfile.write( "Error sending email notification %s.\n" % str(e))
        finally:
            conn.quit()
    except SMTPException as e:
        logfile.write("Error connecting to email server %s.\n" % str(e))

# main
if __name__=='__main__':

    # read credentials
    with open("credentials.json") as f:
        content = json.load(f)
        key = content.get("key")
        secret = content.get("secret")
        org_id = content.get("org_id")
        sender = content.get("sender")
        receiver = content.get("receiver")
        smtp_username = content.get("smtp_username")
        smtp_password = content.get("smtp_password")
        server = content.get("smtp_server")
        subject = content.get("email_subject")
        monitor_interval = content.get("monitor_interval") # monitor interval in seconds
        output_logfile = content.get("logfile") # logfile
        email_alert = content.get("email_alert") # enable or disable email alerts
        max_inactive_interval = content.get("max_inactive_interval")
        debug = content.get("debug")
        f.close()

    # open log file
    output_logfile = output_logfile + str(datetime.now().strftime('_%Y_%m_%d_%H_%M')) + '.log'
    logfile = open(output_logfile, "a")

    if debug:
        print("Output to log file: %s " % output_logfile)

    logfile.write("Umbrella Monitoring Script starting at {}\n".format(datetime.now()))
    logfile.write("Script parameters: {}\n\n".format(json.dumps(content)))

    # Monitor Network Tunnel State for configured interval
    while (True):
        logfile.write("Checking Tunnel Status at {}\n{}\n".format(datetime.now(), "=" * 60))
        monitor_result = get_tunnel_states(key, secret, org_id, max_inactive_interval)
        logfile.write("Update Tunnel States Result: {}\n".format(json.dumps(monitor_result)))

        # if no issues, get_tunnel_states() returns an empty list. If list is not empty,
        # report the error
        if monitor_result:
            logfile.write("Error detected\n")
            if email_alert:
                logfile.write("Email alert enabled, send email alert.\n")
                send_email(server, sender, receiver, subject, monitor_result, smtp_username, smtp_password)
        else:
            logfile.write("No error detected\n")
        logfile.write("Tunnel Status Check completed. Wait {} seconds before next status check.\n\n".format(monitor_interval))
        logfile.flush()
        time.sleep(monitor_interval)
