# Generate an access token for the SPO-RestAPI

import requests
import json
import msal
from cryptography.hazmat.backends import default_backend

def get_access_token_basic_auth(client_id, tenant_id, target_host, username, password, scopes = None, **kwargs):
    if client_id == None:
        print("Missing client_id. Can be found in 'App registrations' in Azure Active Directory. Exiting..")
        AssertionError
    if tenant_id == None:
        print("Missing tenant_id. Can be found in 'Overview' in Azure Active Directory. Exiting..")
        AssertionError
    if target_host == None:
        print("Missing target_host. I.e. <mycompany.sharepoint.com>. Exiting..")
        AssertionError
    if username == None:
        print("Missing username. I.e. <first_name.last_name@<my_company.onmicrosoft.com>. Exiting..")
        AssertionError
    if password == None:
        print("Missing password. Exiting..")
        AssertionError
    if scopes == None:
        logger.info("Using default scope")
        scopes = ["https://" + target_host + "/.default"]
    if type(scopes) != list:
        print("The variable 'scopes' much be a list")
        AssertionError
    authority = "https://login.microsoftonline.com/{}".format(tenant_id)
    if len(kwargs.items()) == 0:
        app = msal.PublicClientApplication(client_id = client_id, authority = authority, **kwargs)
        result = app.acquire_token_by_username_password(username, password, scopes=scopes, **kwargs)
    else:
        app = msal.PublicClientApplication(client_id = client_id, authority = authority)
        result = app.acquire_token_by_username_password(username, password, scopes=scopes)

    try:
        result['access_token']
    except KeyError:
        print("Unexpected response text: {}".format(result))
        raise AssertionError  
    return result

def get_access_token_oath2_secret(client_id, client_secret, tenant_id, target_host, target_identifier):
    if client_id == None:
        print("Missing client_id. Can be found in 'App registrations' in Azure Active Directory. Exiting..")
        AssertionError
    if tenant_id == None:
        print("Missing tenant_id. Can be found in 'Overview' in Azure Active Directory. Exiting..")
        AssertionError
    if client_secret == None:
        print("Missing client_secret. Exiting..")
        AssertionError
    if target_host == None:
        print("Missing target_host. Exiting..")
        AssertionError
    if target_identifier == None:
        print("Missing target_identifier. Exiting..")
        AssertionError

    SO_client_id = client_id + "/" + target_identifier + "@" + tenant_id
    resource     = target_identifier + "/" + target_host + "@" + tenant_id
    data         = {"client_id": SO_client_id, "client_secret": client_secret, "resource": resource,"grant_type": "client_credentials"} 
    url          = "https://accounts.accesscontrol.windows.net/" + tenant_id + "/tokens/OAuth/2"

    req = requests.post(url, headers={'accept': 'application/x-www-form-urlencoded'}, data=data)
    if req.status_code != 200:
        print("Unexpected response status code: %d with response text %s" % (req.status_code, req.text))
        raise AssertionError    
    return req.json()

def cert2string(cert_location):
    backend = default_backend()
    with open(cert_location, 'rb') as f:
        crt_data = f.read()
    return crt_data

def get_access_token_oath2_certificate(client_id, tenant_id, target_host, private_key, thumbprint, scopes = None, **kwargs):
    print(client_id, tenant_id, target_host, private_key, thumbprint, scopes)
    if client_id == None:
        print("Missing client_id. Can be found in 'App registrations' in Azure Active Directory. Exiting..")
        AssertionError
    if tenant_id == None:
        print("Missing tenant_id. Can be found in 'Overview' in Azure Active Directory. Exiting..")
        AssertionError
    if target_host == None:
        print("Missing target_host. Exiting..")
        AssertionError
    if private_key == None:
        print("Missing private_key. Exiting..")
        AssertionError
    if thumbprint == None:
        print("Missing thumbprint. Exiting..")
        AssertionError
    if scopes == None:
        logger.info("Using default scope")
        scopes = ["https://" + target_host + "/.default"]
    if type(scopes) != list:
        print("The variable 'scopes' much be a list")
        AssertionError

    authority = "https://login.microsoftonline.com/" + tenant_id
    client_credential = {"private_key": private_key, "thumbprint": thumbprint}
    app = msal.ConfidentialClientApplication(client_id = client_id, client_credential=client_credential, authority=authority, validate_authority=True, **kwargs)
    result = app.acquire_token_for_client(scopes)
    try:
        result['access_token']
    except KeyError:
        print("Unexpected response text: {}".format(result))
        raise AssertionError    
    return result