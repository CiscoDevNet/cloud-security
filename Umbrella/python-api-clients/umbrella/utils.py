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

import csv
import json
import os
from datetime import datetime

from smtplib import SMTP_SSL as SMTP
from smtplib import SMTPException
from email.mime.text import MIMEText


def get_directory(data_dir):
    ''' Make a directory from the current working directory for the exported data '''
    cwd = os.getcwd() or os.environ.get('CISCO_SAMPLES_DIR')
    print(f"current dir: {cwd}")
    exported_files_dir = cwd + '/' + data_dir
    print(f"exported file dir: {exported_files_dir}")
    try:
        if not os.path.exists(exported_files_dir):
            os.makedirs(exported_files_dir)
        return exported_files_dir
    except Exception as e:
        print(f'Error creating directory for exported data: {e}')

def write_data_to_csv(data, d_filename):
    ''' Write CSV data to file '''
    print(f'Write data to file: {d_filename}')

    try:
        with open(d_filename,'w',encoding='utf-8') as f:
            fieldnames = data[0].keys()

            # Write CSV header
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            # Write CSV data
            for d in data:
                writer.writerow(d)
            f.close()
    except Exception as e:
        raise(e)

def write_data_to_json(data, d_filename):
    ''' Write JSON object file '''
    print(f'Write data to file: {d_filename}')

    try:
        with open(d_filename,'w',encoding='utf-8') as f:
            f.write(json.dumps(data, indent=4))
            f.close()
    except Exception as e:
        raise(e)

def send_email(server, sender, receiver, subject, content, username="", password="", sub_type="plain"):
    ''' Send email notification '''
    text_subtype = sub_type
    content = json.dumps(content, indent=4, sort_keys=True)
    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender # some SMTP servers automatically set up the From field, but not all

        print(f"Try connection to mail server.")
        conn = SMTP(server)
        conn.set_debuglevel(False)
        conn.login(username, password)
        try:
            conn.sendmail(sender, [receiver], msg.as_string())
        except Exception as e:
            print(f"Error sending email notification str(e)")
        finally:
            conn.quit()
    except SMTPException as e:
        print(f"Error connecting to email server str(e)")

def create_log_file(output_logfile, output_sub_dir):
    d_filename = get_directory(output_sub_dir)
    logfile = d_filename + '/' + output_logfile + '.log'
    return logfile

def create_log_file_with_date(output_logfile, output_sub_dir):
    d_filename = get_directory(output_sub_dir)
    logfile = d_filename + '/' + output_logfile + str(datetime.now().strftime('_%Y_%m_%d_%H_%M_%S')) + '.log'
    return logfile
