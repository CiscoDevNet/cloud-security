__author__ = 'yaronca'# encoding = utf-8

import json
import requests
import urllib

from splunklib.data import load
from cim_actions import ModularAction
print dir(ModularAction)

def process_event(helper, *args, **kwargs):
    """
    # IMPORTANT
    # This is a POC and has been run in labs only. Please see this as an example only.
    # Do not remove the anchor macro:start and macro:end lines.
    # These lines are used to generate sample code. If they are
    # removed, the sample code will not be updated when configurations
    # are updated.

    [sample_code_macro:start]

    # Sample code placeholder
    [sample_code_macro:end]
    """

    def _get_corresponding_ip(entity_origin_id):
        # Remember to change URL and creds
        # Receive from parameter (self.configuration.get('url'))
        api_url = 'https://YourAPIServerURLHere.com/api/v2'
        service = 'activities'
        parameter = '?ids={entity_origin_id}'.format(entity_origin_id=entity_origin_id)
        print parameter
        url = '%s/%s%s' % (api_url, service,
                           parameter)
        ## set user-agent
        ua = 'Cloudlock-Incident-Actions-For-Splunk'
        # TODO get token from parameter
        token = 'Bearer EnterYourAPITokenHere'
        ## build headers
        headers   = {
            'user-agent': ua,
           'Authorization': token
        }
        ## make request
        r = requests.get(url, headers=headers)
        helper.log_info({r})
        ## process successful request
        if r.status_code==200:
            return json.loads(r.text)
        return None
        
    def _generate_investigated_incident_event(event, activity, investigate_api_output):
        result = {
        }
        # assuming events are dicts
        result.update(event)
        result.update(activity)
        result.update(investigate_api_output)
        return json.dumps(result)

    input_events = helper.get_events()
    output_events = []

    source_type = "investigated_incident_sourcetype"

    settings = "{}"   # FIXME TBD if other settings needed for env?

    logger = ModularAction.setup_logger('get_context')
    action = ModularAction(settings, logger, 'get_context')
    ip = None
    for i, event in enumerate(input_events):
        helper.log_info("event={}".format(event))

        parsed_event = event
        entity_origin_id = urllib.quote_plus(parsed_event.get("entity_origin_id"))
        helper.log_info(entity_origin_id)
        if entity_origin_id is None:
            helper.log_info("Couldn't extract entity origin id")
            continue
        ra = _get_corresponding_ip(entity_origin_id)
        if ra is None:
            helper.log_info("Couldn't fetch corresponding raw")
            continue
        ip = ra.get('items')[0].get('client_ip')
        helper.log_info(ip)
        if ip is None:
            helper.log_info("Couldn't extract ip from raw")
            continue
            
    action.update(event)
    action.invoke()
    action.writeevents(index='cloudlock', source='get_context')                    
    helper.log_info(ip)                
    investigated_incident = {
        "user": parsed_event.get("entity_owner_email"),
        "incident id": parsed_event.get("id"),
        "origin id": parsed_event.get("entity_origin_id"),
        "source ip": ip,
        "geolocation": ra.get('items')[0].get('client_location'),
        "event name": ra.get('items')[0].get('event_type')
    }
    ev = json.dumps(investigated_incident)
    helper.addevent(ev, sourcetype="investigated_incident_sourcetype")
        
    output_events.append(ev)
    helper.writeevents(output_events)
  
                    
    return 0
