# Migrate Application Lists to a New Organization

With the `application_lists_migrate.py` script, you can make API requests to the Cisco Secure Access Application Lists API in Python. You will need API key credentials for your source Secure Access organization and API key credentials for your target Secure Access organization.

You will create a new set of application lists in the target organization from the application lists in the source organization.

The script follows this workflow:

* Make an API request to get a short-lived access token using your Secure Access API key credentials for the source organization.
* Get the application lists in the organization, and then get the properties of the application lists including the applications and content categories for the applications.
* Write the application lists information from the source organization to a file.
* Make an API request to get a short-lived access token using your Secure Access API key credentials for the target organization.
* Create a new set of application lists in the target organization using the application lists information from the source organization.

## Prerequisites

* Secure Access API key and secret for the source organization.
* Secure Access API key and secret for the target organization.
* Your Secure Access API key and secret must have the permissions to read and write on the `applicationlists` key scope. For more information about the API key scopes, see [API Key Scopes](https://developer.cisco.com/docs/cloud-security/secure-access-api-guides-oauth-2-0-scopes/).
* An installation of the Python runtime environment and an installation of the Python libraries imported by the script.
* Add the values of the script's environment variables to the `.env` file or set the variables in your environment.
    * Set the **OUTPUT_DIR** environment variable—The directory where the script writes the API response to the files.
    * Set the **SOURCE_API_KEY** environment variable—The API key ID for the **source** organization.
    * Set the **SOURCE_API_SECRET** environment variable—The API key secret for the **source** organization.
    * Set the **TARGET_API_KEY** environment variable—The API key ID for the **target** organization.
    * Set the **TARGET_API_SECRET** environment variable—The API key secret for the **target** organization.
* A Python 3.x environment with the following libraries installed:
  * requests
  * oauthlib
  * requests_oauthlib
  * python-dotenv
* You can use the `requirements.txt` file to install the libraries for the script, run:
    `pip install -r requirements.txt`

## Set up a Virtual Environment

Create a Python virtual environment where you will run the `application_lists_migrate.py` script.

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
    python3 application_lists_migrate.py
    ```

## Troubleshooting

1. Ensure that you installed the libraries that are required to run the script.
   An example of the error condition when the libraries have not been installed in the Python environment:

   `ModuleNotFoundError: No module named 'requests'`
1. Ensure that you set up the environment variables in the `.env` file for the script. You can also set the environment variables in the shell where you run the script.
   An example of the error condition when the environment variables are not set:

   `(missing_token) Missing access token parameter.`
