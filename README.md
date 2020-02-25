# SesamUtils

[![Build Status](https://dev.azure.com/sesam-community/Community%20Python%20Packages/_apis/build/status/sesam-community.sesamutils?branchName=master)](https://dev.azure.com/sesam-community/Community%20Python%20Packages/_build/latest?definitionId=1&branchName=master)

**Python module to simplify common tasks when developing microservices for the Sesam integration platform.**


### Usage examples

**Environment Variables**

You can use the VariablesConfig class to load environment variables into your service. It requires a list of required variables. It also support an optional list of variables as a second argument.

```python
from sesamutils import VariablesConfig
import sys

required_env_vars = ["username", "password", "hostname"]
optional_env_vars = ["debug", ("auth_type", "user")] # Default values can be given to optional environment variables by the use of tuples

config = VariablesConfig(required_env_vars, optional_env_vars=optional_env_vars)

if not config.validate():
    sys.exit(1)


print(config.username)

```

**Dotdictify**

A class to help traversing and modifying large nested dictionaries. Lets you navigate by dot notation.

```python
from sesamutils import Dotdictify

example_dict = {
    "test": {
        "my_thing": "hello"
    }
}

dot_dict = Dotdictify(example_dict)

print(dot_dict.test.my_thing)

# hello

```
**Profiler**

 You can use this (A profiling decorator) to see complete details of execution time taken by a function in your program. 
 Based on that, you can optimize your python code if required.

```python
from sesamutils import profiler

@profiler
def <Name of your method>():
    <your method definition>

# Apply to any function with @profiler
# Profiles the function using cProfile, and prints out a report to screen.
# belwo are few lines for illustration  purpose.
ncalls tottime  percall  cumtime  percall filename:lineno(function)
1    0.000    0.000    0.312    0.312 C:/Work/PycharmProjects/node-notification-handler/service/notification-handler.py:143(get_node_members_and_roles)
2    0.000    0.000    0.311    0.156 C:\Users\ravish.ranjan\AppData\Local\Programs\Python\Python36\lib\site-packages\requests\sessions.py:537(get)
2    0.000    0.000    0.311    0.156 C:\Users\ravish.ranjan\AppData\Local\Programs\Python\Python36\lib\site-packages\requests\sessions.py:466(request)
2    0.000    0.000    0.309    0.154 C:\Users\ravish.ranjan\AppData\Local\Programs\Python\Python36\lib\site-packages\requests\sessions.py:617(send)
2    0.000    0.000    0.308    0.154 C:\Users\ravish.ranjan\AppData\Local\Programs\Python\Python36\lib\site-packages\requests\adapters.py:394(send)
2    0.000    0.000    0.306    0.153 C:\Users\ravish.ranjan\AppData\Local\Programs\Python\Python36\lib\site-packages\urllib3\connectionpool.py:446(urlopen)
2    0.000    0.000    0.306    0.153 C:\Users\ravish.ranjan\AppData\Local\Programs\Python\Python36\lib\site-packages\urllib3\connectionpool.py:319(_make_request)
1    0.000    0.000    0.258    0.258 C:\Work\PycharmProjects\node-notification-handler\service\portal.py:34(get_subscription_members)
```

**Sesam Logger**

 You can use this to save time and lines of code. It provides the standard customization of root level logging- 
 configuration and gives you SESAM uniform standard settings.

```python
from sesamutils import sesam_logger

logger = sesam_logger('<name of your module or logger>')
```

Default log level is 'INFO'. To set a different level, you need to provide the environment variable 'LOG_LEVEL'.
Since the microservice log view in the Sesam portal gets it's own timestamps directly from docker, this logger does not print timestamps by default.
However if you want to log timestamps regardless, you can enable timestamps like this:

```python
logger = sesam_logger('<name of your module or logger>', timestamp=True)
```

If your app is using Flask and cherrypy, you can enable request logging by sending the app instance to `sesam_logger` like this:

```python
logger = sesam_logger('<name of your module or logger>', app=<Flask app instance>)
```

**Serve Flask app**

When writing microservices using [Flask](), we don't want to use the built-in development web server as this among other things doesn't set content-length or support chunked encoding (streams).
To mitigate this we use cherrypy to serve our Flask microservices. To simplify this task, you can use our `serve` function:

```python
...
from sesamutils.flask import serve

app = Flask(__name__)

...

if __name__ == "__main__":
    serve(app)
```
To define another port than the default (5000), you can do:
```python
    serve(app, port=<port>)
```

**Sharepoint-online-authentication** 

Library for receiving access tokens for Azure apps. Only supports Sharepoint Online at the moment.


Azure setup:\
1. Create a web-app in Azure Active Directory (ADD):\
  1.1. Enter *New registration* under *App registrations* in ADD and select *Web* under *Redirect URI (optional)*\
  1.2. Set credentials\
    1.2.1. Secret: Enter your newely registered app. Select *Certificates & secrets* in the *manage* view. Click on *New client secret* and copy the Value.\
    1.2.2. Certificate:
      ```
        openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem
      ```
      \
      The line above will (on Ubuntu at least) generate 2 files, cert.pem (public key) and key.prm (private key). 
      Save the private key of the certificate (as a string). Upload the public key of your certifcate (.cer-, .pem- or .crt-file) and copy the thumbprint generated as you upload the public key.\
  1.3. Configure permissions (scopes) for the new app under the *API permissions* view inside the *manage* view of your app. An admin needs to *Grant admin consent for <app_name> to validate the persmissions* 

2. Create a Public-client in Azure Active Directory:\
  2.1. Select *New registration* under *App registrations* in the ADD and select *Public client/native (mobile and desktop)* under *Redirect URI (optional)*\
  2.2. Select the permissions of the app\
  2.3. Select the permissions of different users\
  2.4. Under *Authentication* in your Azure app, set *Treat application as a public client* to *yes* \


##### Functions
###### get_access_token_basic_auth
Obtain access token from username/password authentication
  - Parameters: 
    - client_id:   The client (application) id of the Azure app 
    - tenant_id:   The tenats (directory) id of your Azure instance 
    - target_host: The host-url, i.e. *<my-company>.sharepoint.com* 
    - username:    Your given username, i.e. <my>.<name>@<my-company>.onmicrosoft.com 
    - password:    Your password
    - scopes:      If needed, specify the name of the scope. Should be provided by the Azure admin. If not given, will be set to the default scope. 
    - kwargs:      See docs for [msal.PublicClientApplication](https://msal-python.readthedocs.io/en/latest/)

  - Returns:
    - The autentication payload, including the access token\

###### get_access_token_oath2_secret
Obtain access token from client-secret authentication 
  - Parameters: 
    - client_id:         The client (application) id of the Azure app 
    - client_secret:     The client (application) id of the Azure app 
    - tenant_id:         The tenats (directory) id of your Azure instance 
    - target_host:       The host-url, i.e. *<my-company>.sharepoint.com* 
    - target_identifier: For Sharepoint, this takes the value *00000003-0000-0ff1-ce00-000000000000*

  - Returns:
    - The autentication payload, including the access token\

###### get_access_token_oath2_certificate
Obtain access token from certificate authentication
  - Parameters: 
    - client_id:   The client (application) id of the Azure app 
    - tenant_id:   The tenats (directory) id of your Azure instance 
    - target_host: The host-url, i.e. *<my-company>.sharepoint.com* 
    - private_key: The private key generated (see description above). Must be a valid string. This library also contains a function to convert .pem files to strings if needed (cert2string).
    - thumbprint:  The thumbprint generated when uploading the certificate to Azure.  
    - scopes:      If needed, specify the name of the scope. Should be provided by the Azure admin. If not given, will be set to the default scope. 
    - kwargs:      See docs for [msal.ConfidentialClientApplication](https://msal-python.readthedocs.io/en/latest/)  

  - Returns:
    - The autentication payload, including the access token\

###### cert2string
Convert the content of a certificate to a string
  - Parameters: 
    - cert_location: The location of your private key. 

  - Returns:
    - The private key converted to a string.

### Installation

```python
pip install sesamutils
```
