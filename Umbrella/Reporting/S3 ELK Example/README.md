# General

The following is a basic example of how one could use an ELK stack running in Docker containers to pull Umbrella logs from S3 and build reports/visualisations for this data:
![Example](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/Reporting/S3%20ELK%20Example/umbrellaELK.png)

# *** Important ***

This guide is intended as an example only. For convenience, this guide assumes a simple ELK stack. You should consider putting together your own deployment which will most likely need to include other elements, be appropriately scaled and take into account things like:
* The needed storage.
* The amount of data and how you should deploy/scale the stack elements.
* Bandwidth considerations.
* Security considerations.
* Other environmental considerations.

## Preparations and Prerequisites

* You'll need to be able to run [Docker](https://www.docker.com/) containers.
* You'll need to setup S3 logging in Umbrella and have the key/secret/bucket name available.
* Make sure that you have traffic in your environment and that this traffic is reaching your bucket:

Example using [AWS cli](https://docs.aws.amazon.com/cli/latest/reference/s3/index.html):
```
AWS_ACCESS_KEY_ID=EnterAccessKey AWS_SECRET_ACCESS_KEY=EnterSecretKey aws s3 ls s3://BucketName/FolderOrPrefixName/dnslogs --recursive
```

## Getting Started

Either clone a repo that has an ELK stack, build your own or download the [example](https://github.com/CiscoDevNet/cloudsecurity/raw/master/Umbrella/Reporting/S3%20ELK%20Example/example_stack.tar.gz) (please note that this is just an example - please see the `Important` section above for further information).

* If you are using your own stack, update/replace ../logstash/pipeline/logstash.conf with [this configuration file](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/Reporting/S3%20ELK%20Example/logstash.conf) or the s3 section below:
* Otherwise, if you are using the [example](https://github.com/CiscoDevNet/cloudsecurity/raw/master/Umbrella/Reporting/S3%20ELK%20Example/example_stack.tar.gz):
  * Extract the files in the folder of your choice (```tar -xzvf example_stack.tar.gz```)
  * Edit ../logstash/pipeline/logstash.conf and enter your AWS details under the S3 section (do not change the other settings):

```
s3 {
     access_key_id => "XXX"
     secret_access_key => "XXX"
     bucket => "XXX"
     prefix => "dnslogs/XXX"
     additional_settings => {
       force_path_style => true
       follow_redirects => false
     }
```
* Make sure that you are in the faker folder: ../faker and then run:
```
docker-compose up -d (or to keep up: docker-compose up)
```

## Importing the example reports:
* Kibana will be available at http://localhost:5601
* Goto Management -> Saved Objects
* Import the [reporting example json file](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/Reporting/S3%20ELK%20Example/VisConfig.json) in : Management -> Saved Objects -> Import
