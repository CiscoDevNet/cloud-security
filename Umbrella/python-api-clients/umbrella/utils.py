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
            print(f"keys: {fieldnames}")

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
