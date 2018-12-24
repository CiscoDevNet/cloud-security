# Prerequisites
* Before installing, you must first do the following: 
  - To create an API token, open the Cloudlock Settings > Integrations panel. The token appears in the panel, where it can be selected and copied. Keep the token available, as you will use it in Step 10 of the following Installation process.
![Example](https://github.com/CiscoDevNet/cloud-security/blob/master/Cloudlock/Splunk/Cisco%20Cloudlock%20Splunk%20App/media/auth.png)
  - The Cloudlock Splunk App makes API calls. In order to provide access, please add your IP address to the Whitlist as shown above.
  - Last but not least, please contact support@cloudlock.com to receive your organisations URL. You will need to paste this URL within the Cloudlock Authentication Manager — in step 10 below.


# Installing the Cloudlock Splunk App
To install the Cloudlock Splunk App, follow these steps.

* [Download the Cloudlock Splunk App](https://splunkbase.splunk.com/app/3043/).
* As a Splunk administrator, open the Splunk home page and select the Manage Apps control:

![Example](https://github.com/CiscoDevNet/cloud-security/blob/master/Cloudlock/Splunk/Cisco%20Cloudlock%20Splunk%20App/media/manage_apps.png)
* Select Install app from file:

![Example](https://github.com/CiscoDevNet/cloud-security/blob/master/Cloudlock/Splunk/Cisco%20Cloudlock%20Splunk%20App/media/install_app_browse.png)
* Choose the cloudlock.spl file, then click Upload:
![Example](https://github.com/CiscoDevNet/cloud-security/blob/master/Cloudlock/Splunk/Cisco%20Cloudlock%20Splunk%20App/media/app_install.png)
* When prompted, restart Splunk.
* Click on the Splunk icon in the top left part of the screen.
* The Cloudlock App icon appears on the home screen:

![Example](https://github.com/CiscoDevNet/cloud-security/blob/master/Cloudlock/Splunk/Cisco%20Cloudlock%20Splunk%20App/media/apps.png)
* Select Cloudlock from the Splunk home screen. The following panel opens. Accept the Terms of Service (TOS) and select Submit:
![Example](https://github.com/CiscoDevNet/cloud-security/blob/master/Cloudlock/Splunk/Cisco%20Cloudlock%20Splunk%20App/media/auth_splunk.png)
* Enter the following information
  - Name: admin
  - URL: the URL you received from Cloudlock Support in the Prerequisites step.
  - Token: the token generated in the Prerequisites step.
Note: If the URL provided is not: `https://api.cloudlock.com/api/v2` then you will need to also modify the data input (Settings -> Data Input -> CloudLock Incident Extraction -> incidents and then change the url). For example:
![Example](https://github.com/CiscoDevNet/cloud-security/blob/master/Cloudlock/Splunk/Cisco%20Cloudlock%20Splunk%20App/media/app_url.png)

Select App: Cloudlock > Cloudlock Incident Overview:
![Example](https://github.com/CiscoDevNet/cloud-security/blob/master/Cloudlock/Splunk/Cisco%20Cloudlock%20Splunk%20App/media/db1.png)

The Incident Overview dashboard begins to display data. You have finished installing the Cloudlock Splunk app.


# Using the Cloudlock Splunk App
The following sections detail use of the Cloudlock Splunk app. Note that the data displays in the app refresh every 3 minutes. 
You access the Cloudlock Splunk app from the Splunk home screen:



When the app opens the Cloudlock Incident Overview panel is displayed. If the panel displays no data it may indicate an installation failure; refer to the above section Installing the Cloudlock Splunk App to repeat the process. 

The Cloudlock Incident Overview page gives you an overview of Cloudlock Incidents. The top panels give a current daily or hourly total incidents in each status state (New, In Progress, Resolved, or Dismissed):



Other data displays show the top offenders (by incident count) as well as a chart of incidents per platform:

Managing Incidents
To manage incidents in the Cloudlock Splunk App, follow these steps:

In Splunk, select App:Cloudlock > Incidents > Incident Management



The Incidents List appears. You can manage incidents in the list in several ways:


Filter the list by Severity, Status or Time by using the selectors at the top of the list:


Update the Status or Severity of an incident by selecting the new value, then and select Update on the right:


Review details of an incident by selecting it. The Incident Details panel appears. From this panel you can email the owner of the object in violation and (with appropriate credentials) view the object itself:

Enabling User Access to the App
The Cloudlock Splunk app is installed and run by a Splunk administrator. However, you can enable a non-administrator to use it by adding the following capabilities to a new or existing role:

# TOS
© 2018 Cisco and/or its affiliates. All rights reserved.  Cloudlock is a registered trademark of Cisco. All other trademarks or other third party brand or product names included herein are the trademarks or registered trademarks of their respective companies or organizations and are used only for identification or explanation.
Cisco Cloudlock and related documentation are protected by contract law, intellectual property laws and international treaties, and are authorized for use only by customers for internal purposes in accordance with the applicable subscription agreement or terms of service. This documentation may not be distributed to third parties.  
This documentation is provided “as is” and all express or implied conditions, representations and warranties, including implied warranty of merchantability, fitness for a particular purpose or non-infringement are hereby disclaimed, except to the extent that such disclaimers are held to be legally invalid.  
The information contained in this documentation is subject to change without notice.  Cisco recommends you periodically check this site to ensure you are utilizing the most current version of this documentation.
Add or select the user, then add the roles cloudlock_read and cloudlock_write to the inheritance list:


The inherited capabilities will resemble this:


Add the cloudlock index to the list of indexes and indexes searched by default:

The user now has access to the Cloudlock Splunk App.
