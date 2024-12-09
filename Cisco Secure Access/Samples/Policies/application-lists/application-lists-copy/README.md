# Copy Application Lists in an Organization

With the `application_lists_copy.py` script, you can make API requests to the Cisco Secure Access Application Lists API in Python. You will need API key credentials for your organization to create a new set of application lists in the organization from the application lists in the organization.

The script follows this workflow:

* Make an API request to get a short-lived access token using your Secure Access API key credentials for the organization.
* Get the application lists in the organization, and then get the properties of the application lists including the applications and content categories for the applications.
* Write the application lists information from the organization to a file.
* Create a new set of application lists in the organization. The new application lists will have a randomly generated number prepended to the name of the application lists.

## Prerequisites

* Secure Access API key and secret.
* Your Secure Access API key and secret must have the permissions to read and write on the `applicationlists` key scope. For more information about the API key scopes, see [API Key Scopes](https://developer.cisco.com/docs/cloud-security/secure-access-api-guides-oauth-2-0-scopes/).
* An installation of the Python runtime environment and an installation of the Python libraries required by the script.
* Add the values of the script's environment variables to the `.env` file or set the variables in your environment.
    * Set the **OUTPUT_DIR** environment variable to the directory where the script should write the API response to the files.
    * Set the **API_KEY** environment variable to the your Secure Access API key ID.
    * Set the **API_SECRET** environment variable to your Secure Access API key secret.
* A Python 3.x environment with the following libraries installed:
  * requests
  * oauthlib
  * requests_oauthlib
  * python-dotenv
* You can use the `requirements.txt` file to install the libraries for the script, run:
    `pip install -r requirements.txt`

## Set up a Virtual Environment

Create a Python virtual environment where you will run the `application_lists_copy.py` script.

1. Run:
    ```shell
    python3 -m venv myenv
    ```
1. (Windows) Run:
    ```shell
    myenv\\Scripts\\activate
    ```
1. (macOS) Run:
    ```shell
    source myenv/bin/activate
    ```

## Run the Script

1. Run:
    ```shell
    python3 application_lists_copy.py
    ```

## Troubleshooting

1. Ensure that you installed the libraries that are required to run the script.
   An example of the error condition when the libraries have not been installed in the Python environment:

   `ModuleNotFoundError: No module named 'requests'`
1. Ensure that you set up the environment variables in the `.env` file for the script. You can also set the environment variables in the shell where you run the script.
   An example of the error condition when the environment variables are not set:

   `(missing_token) Missing access token parameter.`
