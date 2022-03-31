# General

The following is an example of how to use an [ELK stack](https://www.elastic.co/elk-stack) running in Docker containers to pull Umbrella security activity, enrich it with the Investigate API and build reports or visualisations for this data:
![Example](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/Samples/Reports/Reporting-and-Investigate-APIs-ELK/dash1.png)

## What to Consider

This guide is intended as an example only. For convenience, this guide assumes a simple ELK stack. You should consider putting together your own deployment which will most likely need to include other elements, be appropriately scaled and take into account things like:

* The needed storage.
* The amount of data and how you should deploy/scale the stack elements.
* Bandwidth considerations.
* Security considerations.
* Other environmental considerations.

## Preparations and Prerequisites

* You'll need to be able to run Docker containers.
* You'll need to generate your [Reporting API](https://docs.umbrella.com/umbrella-api/docs/authentication-and-errors) and [Investigate API](https://docs.umbrella.com/investigate-api/docs/about-the-api-authentication) tokens in Umbrella and have these available.
* Make sure that you have traffic in your environment (security related traffic).

## Getting Started

* Download this sample:

```shell
svn export https://github.com/CiscoDevNet/cloud-security/trunk/Umbrella/Samples/Reports/Reporting-and-Investigate-APIs-ELK
```

* Decompress it:

```shell
cd Reporting\ and\ Investigate\ APIs\ in\ ELK/
unzip Reporting_Investigate_ELK.zip
cd Reporting_Investigate_ELK
```

* Edit the configuration and environment file:

```shell
vim .env
```

Inside you will need to change the placeholders based on your environment:

```none
UMBRELLA_ORG_ID=EnterYourOrgID (you can see this in your dashboard)
UMBRELLA_REPORTING_START_TS=EnterStartTimeStamp - please see the note below 
INVESTIGATE_TOKEN=EnterInvestigateAPIToken (please see the Preperations section above)
UMBRELLA_REPORTING_API_TOKEN=EnterReportingAPIToken (please see the Preperations section above)
```

* Note: The reporting API requires a [start time parameter](https://docs.umbrella.com/umbrella-api/docs/security-activity-report).

* Start the containers:

```shell
sudo -E docker-compose up
```

## Import the Example Reports

* Kibana will be available at http://localhost:5601
* Import the [dashboard example json file](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/Samples/Reports/Reporting-and-Investigate-APIs-ELK/Umbrella_Dashboard.json) in : Management -> Saved Objects -> Import
* Open the Dashboard -> Cisco Umbrella Security Dashboard
