#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               "https://developer.cisco.com/docs/licenses"
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
from email.mime.text import MIMEText
from datetime import datetime
import json, time

def get_tunnel_states(key,secret,orgid,max_inactive_interval):
    global last_tunnels

    logfile.write("Sending Requests.......\n")
    response = requests.get(
        url="https://management.api.umbrella.com/v1/organizations/{organizationId}/tunnelsState".format(organizationId=orgid),
        headers={"Content-Type":"application/json"},
        auth=(key,secret))
    logfile.write("Response: Status = {}, Message Content = {}\n".format(response.status_code, response.text))

    # Report Error if Response is not 200/OK
    if not response.ok:
        #response.raise_for_status()
        logfile.write("ERROR: Response Status is not 200OK \n")
        return (json.loads(f'{{"update status": "Script fail", "reason": "ERROR: API Request fail, status = {response.status_code}" }}'))

    tmp = []
    for tunnel in response.json():
        tunnel_id = tunnel.get("tunnelId")
        logfile.write("Checking Tunnel state for {}.\n".format(tunnel_id))

        if tunnel.get("status") != "UP":
            logfile.write("Tunnel {} state is {}.\n".format(tunnel_id, tunnel.get("status")))
            #Tunnel state is not UP, somethig is wrong
            tunnel["monitor_result"] = tunnel.get("status")
            tmp.append(tunnel)
        else:
            #Tunnel state is UP, we will check it with last status
            last_modified_timestamp = datetime.strptime( tunnel.get("modifiedAt")[:-4], "%Y-%m-%dT%H:%M:%S.%f")
            delta_since_last_update = (datetime.utcnow()-last_modified_timestamp).total_seconds()
            logfile.write("Tunnel {} last state update {} seconds ago.  ".format(tunnel_id, delta_since_last_update))

            #if last "modifiedAt" time delta is greater than configured MAX_INACTIVE_INTERVAL, then the tunnel is INACTIVE
            if delta_since_last_update > max_inactive_interval:
                logfile.write("Tunnel is UP but INACTIVE.\n")
                tunnel["monitor_result"] = "UP_BUT_INACTIVE"
                tmp.append(tunnel)
            else:
                logfile.write( "Tunnel UP and ACTIVE.\n".format(tunnel_id, delta_since_last_update))

    return tmp

def send_email(server,sender,receiver,subject,content,username="",password="",sub_type="plain"):

    text_subtype = sub_type
    content=json.dumps(content,indent=4,sort_keys=True)
    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender # some SMTP servers will do this automatically, not all

        conn = SMTP(server)
        conn.set_debuglevel(False)
        conn.login(username, password)
        try:
            conn.sendmail(sender, [receiver], msg.as_string())
        finally:
            conn.quit()

    except Exception as e:
        return

if __name__=='__main__':

    with open("credentials.json") as f:
        content = json.load(f)
        key = content.get("key")
        secret = content.get("secret")
        orgid = content.get("orgid")
        sender = content.get("sender")
        receiver = content.get("receiver")
        smtp_username = content.get("smtp_username")
        smtp_password = content.get("smtp_password")
        server = content.get("smtp_server")
        subject = content.get("email_subject")
        monitor_interval = int(content.get("monitor_interval"))         # monitor interval in seconds
        output_logfile = content.get("output_logfile")
        email_alert = bool(content.get("email_alert"))
        max_inactive_interval = int(content.get("max_inactive_interval"))

        f.close()

    logfile = open(output_logfile, "a")
    logfile.write("Umbrella Monitoring Script starting at {}\n".format(datetime.now()))
    logfile.write("Scritp parameters: {}\n\n".format(json.dumps(content)))

    while (True):
        logfile.write("Checking Tunnel Status at {}\n{}\n".format(datetime.now(), "=" * 60))

        monitor_result = get_tunnel_states(key,secret,orgid,max_inactive_interval)
        logfile.write("Update Tunnel States Result: {}\n".format(json.dumps(monitor_result)))

        # if no issues, get_tunnel_states() will return empty list. If list is not empty, something
        # is wrong and we need to report
        if (monitor_result):
            logfile.write("======>Error detected!\n")
            if (email_alert):
                logfile.write("Sending email alert!\n")
                send_email(server,sender,receiver,subject,monitor_result,smtp_username,smtp_password)
        else:
            logfile.write("=======>No error detected!\n")
        logfile.write("Checking completed. Wait {} seconds for next check...\n\n".format(monitor_interval))
        logfile.flush()
        time.sleep(monitor_interval)
