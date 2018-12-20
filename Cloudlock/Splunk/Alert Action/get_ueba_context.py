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
    # Do not remove the anchor macro:start and macro:end lines.
    # These lines are used to generate sample code. If they are
    # removed, the sample code will not be updated when configurations
    # are updated.

    [sample_code_macro:start]

    # The following example gets the alert action parameters and prints them to the log
    get_context = helper.get_param("get_context")
    helper.log_info("get_context={}".format(get_context))


    # The following example adds two sample events ("hello", "world")
    # and writes them to Splunk
    # NOTE: Call helper.writeevents() only once after all events
    # have been added
    helper.addevent("hello", sourcetype="sample_sourcetype")
    helper.addevent("world", sourcetype="sample_sourcetype")
    helper.writeevents(index="summary", host="localhost", source="localhost")

    # The following example gets the events that trigger the alert
    events = helper.get_events()
    for event in events:
        helper.log_info("event={}".format(event))

    # helper.settings is a dict that includes environment configuration
    # Example usage: helper.settings["server_uri"]
    helper.log_info("server_uri={}".format(helper.settings["server_uri"]))
    [sample_code_macro:end]
    """

    def _get_corresponding_app(entity_id):
        # TODO receive from parameter (self.configuration.get('url'))
        api_url = 'https://api-demo.cloudlockng.com/api/v2'
        service = 'installs'
        #parameter = '?ids=8:aws:S3:{origin_id}'.format(origin_id=origin_id)
        parameter = '{entity_id}'.format(entity_id=entity_id)
        print parameter
        url = '%s/%s/%s' % (api_url, service,
                            urllib.quote_plus(parameter))
        ## set user-agent
        ua = 'Cloudlock-Incident-Actions-For-Splunk'
        # TODO get token from parameter
        token = 'Bearer b217748e-1dca-4b9a-9b26-6fe1a94cd725'
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

    def _get_corresponding_ip(entity_origin_id):
        #helper.log_info("Start ip")
        # TODO receive from parameter (self.configuration.get('url'))
        api_url = 'https://api-demo.cloudlockng.com/api/v2'
        #helper.log_info(api_url)
        service = 'activities'
        #helper.log_info(service)
        #parameter = '?ids=8:aws:S3:{origin_id}'.format(origin_id=origin_id)
        parameter = '?ids={entity_origin_id}'.format(entity_origin_id=entity_origin_id)
        print parameter
        #helper.log_info(parameter)
        url = '%s/%s%s' % (api_url, service,
                           parameter)
        #helper.log_info(url)
        ## set user-agent
        ua = 'Cloudlock-Incident-Actions-For-Splunk'
        # TODO get token from parameter
        token = 'Bearer b217748e-1dca-4b9a-9b26-6fe1a94cd725'
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

#    limit = 100     # FIXME get from configuration

    settings = "{}"   # FIXME what should this be?

    logger = ModularAction.setup_logger('get_context')
    action = ModularAction(settings, logger, 'get_context')
    #helper.log_info("Before Start Loop")
    ip = None
    for i, event in enumerate(input_events):
        helper.log_info("event={}".format(event))

        parsed_event = event
        # TODO verify
        entity_origin_id = urllib.quote_plus(parsed_event.get("entity_origin_id"))
        helper.log_info(entity_origin_id)
        if entity_origin_id is None:
            helper.log_info("Couldn't extract entity origin id")
            continue
        #helper.log_info("Entity ID is:")
        #helper.log_info(entity_id)
        ra = _get_corresponding_ip(entity_origin_id)
        #helper.log_info("The raw data is:")
        #helper.log_info(ra)
        if ra is None:
            helper.log_info("Couldn't fetch corresponding raw")
            continue
        #helper.log_info(ra.get('items')[0].get('client_ip'))
        ip = ra.get('items')[0].get('client_ip')
        helper.log_info(ip)
        if ip is None:
            helper.log_info("Couldn't extract ip from raw")
            continue
        #helper.log_info("Got entity_id: {}".format(entity_id))
        
    #helper.log_info("Before update event")
    action.update(event)
    action.invoke()
    #helper.log_info("Before add event")
    #action.addevent(json.dumps(result), sourcetype=source_type)
    #helper.log_info("Not adding event here")

    action.writeevents(index='cloudlock', source='get_context')
    #helper.log_info("Not writing events here")


    #previous commented out block
    
        
        # Extract the App Risk
        # TODO verify
        
    #helper.log_info("Got app risk: {}".format(risk))
            
        #investitate_ip_output = _invoke_investigate_api(source_ip)
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
    #helper.log_info(dir(helper))                
    helper.writeevents(output_events)
    #helper.addinfo(output_events)
    #helper.update(output_events)
    
                    
    return 0
