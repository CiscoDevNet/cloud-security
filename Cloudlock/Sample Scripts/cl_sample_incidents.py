#! /usr/bin/python
"""
This is a simple demo of connecting and working with the CloudLock API.

Copyright (c) 2019 Cisco and/or its affiliates.

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

import argparse
from time import sleep
import collections
from datetime import datetime
import logging
import logging.handlers
import sys
from contextlib import contextmanager
import os
import json

import requests
from configparser import ConfigParser, NoOptionError
from requests.packages.urllib3.util import Retry


# Requests 2.7.0 has a problem with SSL certificate validation (it's integration with urllib3).
KEY_AND_VALUE_CHANGE = 3
KEY_CHANGE_ONLY = 2
MATCHES_LIMIT = 10

requests.packages.urllib3.disable_warnings()

EventIndex = collections.namedtuple('EventIndex', ['datetime', 'offset'])

_local_dir_path = os.path.dirname(os.path.realpath(__file__))

MISSING_FIELD_TEXT = 'na'


class CLAPIClient(object):
    """
    CloudLock API Client
    """
    BASE_URL = 'https://api.cloudlock.com/api/v2'

    def __init__(self, token, base_url=BASE_URL):
        self.token = token
        self.base_url = base_url
        self.session = session = requests.session()
        retries = Retry(total=100, status_forcelist=(429, 500, 502, 504), backoff_factor=0.1)
        session.mount(self.base_url, requests.adapters.HTTPAdapter(max_retries=retries))
        session.headers.update(
            {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(self.token)})

    @staticmethod
    def to_datetime(value):
        try:
            return datetime.strptime(value[:-6], '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')

    @staticmethod
    def get_latest_incident(results, order='created_at'):
        latest_created_at = results[-1][order]
        last_second = CLAPIClient.to_datetime(latest_created_at)
        offset = len(
            filter(lambda x: last_second == CLAPIClient.to_datetime(x[order]), results))
        return EventIndex(latest_created_at, offset)

    def _request(self, relative_url, params=None, data=None, method='GET', verify_ssl=False):
        relative_url = '/'.join((self.base_url, relative_url))

        response = self.session.request(method, relative_url, params=params, data=data,
                                        verify=verify_ssl)

        response.raise_for_status()

        return response.json()

    def get_incidents(self, **payload):
        return self._request('incidents?count_total=false', params=payload)['items']

    def get_incident(self, incident_id, **payload):
        r = self._request('incidents/%s' % incident_id, params=payload)
        incident = r['results'][0]
        return incident

    def update_incident(self, incident_id, status=None, severity=None, customer_key=None):
        data = {'incident_status': status, 'severity': severity, 'customer_key': customer_key}
        data = {(k, v) for k, v in data if v is not None}
        self._request('incidents/{}'.format(incident_id), data=json.dumps(data), method='PUT')

    def get_all_incidents(self, incident_index, limit=100, order='created_at', vendor=None):
        while True:
            logging.info('Getting last incidents from {} (offset {})'.format(*incident_index))
            # Removing timezone
            dt_ntz = None
            created_after = None
            updated_after = None
            if incident_index.datetime:
                dt = CLAPIClient.to_datetime(incident_index.datetime)
                dt_ntz = unicode(dt.replace(tzinfo=None))
            if order == 'created_at':
                created_after = dt_ntz
            else:
                updated_after = dt_ntz

            results = self.get_incidents(created_after=created_after, offset=incident_index.offset,
                                         limit=limit, order=order, updated_after=updated_after,
                                         vendor=vendor)
            if not results:
                logging.info('No new incidents found')
                raise StopIteration()

            logging.info('{} new incidents found'.format(len(results)))
            incident_index = self.get_latest_incident(results, order)
            yield incident_index, results


class Recorder(object):
    """
    stores latest polling data. implemented with python config parser.
    """
    config_section = 'CL_POLLING'

    def __init__(self):
        self.file = os.path.join(_local_dir_path, 'cl_polling.ini')
        self.config = ConfigParser(allow_no_value=True)
        self.config.read(self.file)
        if not self.config.has_section(self.config_section):
            with open(self.file, 'w') as f:
                self.config.add_section(self.config_section)
                self.config.set(self.config_section, 'Empty', None)
                self.config.write(f)
            self.config.read(self.file)

    def save(self, key, value):
        with open(self.file, 'w') as f:
            self.config.set(self.config_section, str(key), str(value))
            self.config.write(f)

    def get(self, key, is_int=False):
        try:
            func = self.config.getint if is_int else self.config.get
            return func(self.config_section, key)
        except (NoOptionError, ValueError):
            return None

    def get_last_call(self):
        last_call = self.get('last_call')
        last_call = last_call if last_call and last_call != u'None' else None
        last_offset = self.get('last_offset', is_int=True)

        return EventIndex(last_call, last_offset)

    def save_last_call(self, event_index):
        dt_tz = CLAPIClient.to_datetime(event_index.datetime)
        dt = dt_tz.replace(tzinfo=None)
        self.save('last_call', unicode(dt))
        self.save('last_offset', event_index.offset)


def incidents_loop(cl_client, output_client, recorder, last_event, limit=100, order='created_at',
                   vendor=None):
    """
    Gets incidents from Cloudlock API and pushes the to local log client

    :param cl_client: CloudLock api client (CLAPClient)
    :param siem_client: writes the incidents into the requested log client.
    :param recorder: writes the latest logged incident
    :param last_event: date to get incidents from.
    :param limit: the max items to be retrieved in a query
    :param order: to order to read the results
    """
    incidents_from_query = cl_client.get_all_incidents(last_event, limit=limit, order=order,
                                                       vendor=vendor)
    for last_date, incidents in incidents_from_query:
        output_client.write(incidents)
        recorder.save_last_call(last_date)


def run_forever(polling_interval, fn, cl_client, output_client, recorder, last_event,
                limit, order, vendor):
    """
    Runs function forever in on a defined interval.
    :param polling_interval: interval between each run
    :param fn: function to run
    :param args: that function arguments
    """
    while True:
        fn(cl_client, output_client, recorder, last_event, limit, order, vendor)
        last_event = recorder.get_last_call()
        logging.info('No new results found sleeping for {} seconds'.format(polling_interval))
        sleep(polling_interval)


def config_log(loglevel):
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
    numeric_level = getattr(logging, loglevel.upper(), None)
    if numeric_level is None:
        raise ValueError('Invalid log level: {}'.format(loglevel))
    logging.root.setLevel(numeric_level)


def init_argparse():
    parser = argparse.ArgumentParser(
        description='Demo for working with incidents by utilizing CloudLocks API',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--siem_client', choices=output_clients, required=True,
                        help='The SIEM client that you are using')
    parser.add_argument('-t', '--token', required=True,
                        help='The user personal CloudLock token from the integrations tab')
    parser.add_argument('-u', '--url', help='Base url to CloudLock api server (for internal use)')
    parser.add_argument('-p', '--output_dir_path',
                        help='The output dir of the script (when using file output)')
    parser.add_argument('-f', '--from_date', default=None,
                        help='Start polling from specific date, this overwrites the'
                             "saved last called in the following format: 'YYYY-MM-DD HH:mm:ss.f'")
    parser.add_argument('-l', '--log_level', default='INFO',
                        help='Log verbosity level. Default is INFO.')
    parser.add_argument('-i', '--polling_interval', type=int,
                        help='The polling interval (secs) in polling mode. If provided, '
                             'runs script forever, polling for new events.')
    parser.add_argument('-o', '--order', default='created_at',
                        help='The order of the polling')
    parser.add_argument('--client_address',
                        help='The address the client is listening on (when using syslog)'
                             ' - <address>:<port>.',
                        default='localhost:514')
    parser.add_argument('--limit', default=100, help=argparse.SUPPRESS)
    parser.add_argument('--file_format', default=None,
                        choices=output_clients, help=argparse.SUPPRESS)
    parser.add_argument('--vendor', default=None, help=argparse.SUPPRESS)
    parser.add_argument('--clear_unicode', default=False, help='Clear unicode prefix', nargs='?',
                        const=True)
#    parser.add_argument('--limit',
#                        default=100, help='The number of incidents that should be polled')
    return parser


def extract_args(parser):
    args = parser.parse_args()
    address = args.client_address.split(':')
    args.client_address = address[0], int(address[1])
    return args


severity_mapping = {'INFO': 1, 'WARNING': 3, 'ALERT': 5, 'CRITICAL': 10}

leef_event_attr_mapping = (
    ('id', 'CloudLockID'),
    ('customer_key', 'group'),
    ('incident_status', 'cat'),
    ('severity', 'sev', lambda sev: severity_mapping[sev]),
    ('created_at', 'devTime'),
    ('updated_at', 'updated_at'),
    ('match_count', 'match_count'),
    ('entity.id', 'entity_id'),
    ('entity.name', 'resource'),
    ('entity.mime_type', 'entity_mime_type'),
    ('entity.owner_email', 'entity_owner_email'),
    ('entity.owner_name', 'usrName'),
    ('entity.origin_id', 'entity_origin_id'),
    ('entity.origin_type', 'entity_origin_type'),
    ('entity.direct_url', 'url'),
    ('entity.vendor.name', 'realm'),
    ('policy.id', 'policy_id'),
    ('policy.name', 'policy'),
)

cef_event_attr_mapping = (
    ('entity.name', 'name'),
    ('severity', 'severity', lambda sev: severity_mapping[sev]),
    ('id', 'externalID'),
    ('customer_key', 'msg'),
    ('incident_status', 'cat'),
    ('created_at', 'start'),
    ('updated_at', 'updated_at'),
    ('match_count', 'cnt'),
    ('entity.id', 'entity_id'),
    ('entity.mime_type', 'entity_mime_type'),
    ('entity.owner_email', 'suser'),
    ('entity.owner_name', 'fname'),
    ('entity.origin_id', 'entity_origin_id'),
    ('entity.origin_type', 'fileType'),
    ('entity.direct_url', 'request'),
    ('policy.id', 'policy_id'),
    ('policy.name', 'reason'),
)


def flatten(d, do_matches_limit=True, remove_unicode=False, parent_key='', sep='_'):
    items = []
    for k, v in d.iteritems():
        new_key = parent_key + sep + k if parent_key else k
        new_key_formatted = format_unicode_string(new_key, remove_unicode)
        if k == u'matches':
            v = handle_matches(v, do_matches_limit=do_matches_limit, remove_unicode=remove_unicode)
        else:
            v = format_unicode_string(v, remove_unicode)
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, do_matches_limit=do_matches_limit,
                                 remove_unicode=remove_unicode,
                                 parent_key=new_key_formatted,
                                 sep=sep).items())
        else:
            items.append((new_key_formatted, v))
    return dict(items)


def format_unicode_string(s, remove_unicode):
    if remove_unicode and isinstance(s, unicode):
        result = s.encode('utf-8')
    else:
        result = s
    return result


def format_unicode_dict(d, remove_unicode):
    new_dict = {}
    for k, v in d.iteritems():
        if isinstance(v, dict):
            new_dict[format_unicode_string(k, remove_unicode)] = \
                format_unicode_dict(v, remove_unicode)
        else:
            new_dict[format_unicode_string(k, remove_unicode)] = \
                format_unicode_string(v, remove_unicode)
    return new_dict


def handle_matches(matches, do_matches_limit, remove_unicode):
    if do_matches_limit:
        new_match_list = []
        match_count = 0
        for match in matches:
            match_count += 1
            if match_count > MATCHES_LIMIT:
                new_match_list.append({format_unicode_string(u'match_limit', remove_unicode): True})
                break
            else:
                new_match_list.append(format_unicode_dict(match, remove_unicode))
    else:
        new_match_list = matches
    return new_match_list


mapping_types = {
    KEY_CHANGE_ONLY: lambda data, old_key, new_key: (new_key, data[old_key]),
    KEY_AND_VALUE_CHANGE: lambda data, old_key, new_key, convert: (new_key, convert(data[old_key]))
}


def transform_dict(mapping, data):
    flat_data = flatten(data, do_matches_limit=True, remove_unicode=False, parent_key='', sep='.')
    for mapper in mapping:
        mapper_type = len(mapper)
        extract_fn = mapping_types[mapper_type]
        if mapper[0] in flat_data:
            new_key, value = extract_fn(flat_data, *mapper)
            yield new_key, value
        else:
            yield mapper[1], MISSING_FIELD_TEXT


class FileClient(object):
    def __init__(self, formatter, output_dir_path=None):
        """
        :param formatter: a callable that formats a single item.
        :param dir_path: the dir path to write the file to.
        """
        self.file_path = os.path.join(output_dir_path or _local_dir_path, 'siem.json')
        self.formatter = formatter

    def write(self, items):
        with open(self.file_path, 'a') as f:
            for item in items:
                formatted_item = json.dumps(self.formatter(item, do_matches_limit=False,
                                                           remove_unicode=False))
                f.write(formatted_item + '\n')


class SyslogClient(object):
    clear_unicode = False

    def __init__(self, formatter, clear_unicode, client_address=('localhost', 514)):
        """
        :param formatter: a callable that formats a single item.
        :param address: a tuple representing the address the client is listening on.
        """
        self.formatter = formatter
        self.clear_unicode = clear_unicode
        self.syslog_logger = syslog_logger = logging.getLogger('SyslogClient')
        syslog_logger.propagate = False
        syslog_logger.setLevel(logging.INFO)
        handler = logging.handlers.SysLogHandler(address=client_address)
        handler.formatter = logging.Formatter('%(message)s')
        syslog_logger.addHandler(handler)

    def write(self, items):
        for item in items:
            if self.formatter is flatten and self.clear_unicode:
                item_text = str(self.formatter(item, do_matches_limit=True,
                                               remove_unicode=self.clear_unicode))
                item_text = item_text.replace('None', 'null')
                item_text = item_text.replace('\'', '\"')
                self.syslog_logger.info(item_text)
            else:
                self.syslog_logger.info(self.formatter(item))


def leef_formatter(item):
    t_item = dict(transform_dict(leef_event_attr_mapping, item))
    leef_header = u'LEEF:1.0|Cloudlock|API|v2|Incidents|'
    event_attr = u'\t'.join(u'{}={}'.format(k, v) for k, v in t_item.iteritems())
    event_attr += u'\tdevTimeFormat=yyyy-MM-ddTHH:mm:ss.SSSSSSZ'
    return leef_header + event_attr


def cef_formatter(item):
    t_item = dict(transform_dict(cef_event_attr_mapping, item))
    cef_header = u'CEF:0|Cloudlock|API|v2|CloudLockEnterpriseAPI|{}|{}|'.format(
        t_item.pop('name'), t_item.pop('severity'))
    event_attr = u' '.join(u'{}={}'.format(k, v) for k, v in t_item.iteritems())
    return cef_header + event_attr


def get_output_client(cmdline_args):
    client, formatter = output_clients[cmdline_args.siem_client]
    client_args = {arg: getattr(cmdline_args, arg) for arg in clients_args[client]}
    if client == FileClient:
        if cmdline_args.file_format is not None:
            formatter = output_clients[cmdline_args.file_format][1]
        return client(formatter, **client_args)
    else:
        return client(formatter, clear_unicode=cmdline_args.clear_unicode, **client_args)


clients_args = {
    SyslogClient: ('client_address',),
    FileClient: ('output_dir_path',),
}

output_clients = {
    'qradar': (SyslogClient, leef_formatter),
    'arcsight': (SyslogClient, cef_formatter),
    'flat_syslog': (SyslogClient, flatten),
    'flat_file': (FileClient, flatten),
}


def main():
    args = extract_args(init_argparse())
    config_log(args.log_level)

    cl_client = CLAPIClient(args.token, args.url)
    recorder = Recorder()
    output_client = get_output_client(args)

    last_event = EventIndex(args.from_date, 0) if args.from_date else recorder.get_last_call()

    logging.info('Polling from {}'.format(last_event.datetime or 'first known event'))

    if args.polling_interval:
        run_forever(args.polling_interval, incidents_loop, cl_client, output_client, recorder,
                    last_event, args.limit, args.order, args.vendor)
    else:
        incidents_loop(cl_client, output_client, recorder,
                    last_event, args.limit, args.order, args.vendor)
    logging.info('Finished pulling incidents, exiting...')


@contextmanager
def file_lock(lock_file):
    """
    Creates a lock file to prevent the script from having more than one instance running
    :param lock_file: lock file name
    """
    if os.path.exists(os.path.join(_local_dir_path, 'lock')):
        logging.error('Could not get lock. Is there another script instance running?'.format())
        sys.exit(1)
    else:
        with open(lock_file, 'w') as f:
            f.write('1')
        try:
            yield
        finally:
            os.remove(lock_file)


if __name__ == '__main__':
    with file_lock('lock'):
        try:
            main()
        except KeyboardInterrupt:
            logging.info('You pressed ctrl+c, exiting gracefully')
        except Exception as e:
            logging.error('Unexpected error occurred:')
            logging.exception(e)
            sys.exit(1)
