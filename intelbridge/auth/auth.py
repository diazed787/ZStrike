"""
auth.py
Methods for authenticating to Falcon and Zscaler APIs
"""
import logging
import configparser
import requests
import time
import json
import base64
from util.util import log_http_error
from falconpy import APIHarness


config = configparser.ConfigParser()
config.read('config.ini')
cs_config = config['CROWDSTRIKE']
cs_client = str(cs_config['client'])
cs_secret = str(cs_config['secret'])
cs_base_url = str(cs_config['base_url'])
zs_config = config['ZSCALER']
zs_vanity = str(zs_config['auth_hostname'])
zs_client_id = str(zs_config['client_id'])
zs_client_secret = str(zs_config['client_secret'])

def cs_auth():
    """Returns a new Falcon API Auth Token, hot off the press
    returns: Falcon API Auth token
    """
    logging.info(f"Authenticating client {cs_client} to Falcon API")
    # url = f"{cs_base_url}/oauth2/token"
    # data = f"client_id={cs_client}&client_secret={cs_secret}"
    # headers = {'content-type': 'application/x-www-form-urlencoded'}
    # response = requests.post(url=url, data=data, headers=headers)
    # try:
    #     response.raise_for_status()
    # except requests.exceptions.HTTPError as err:
    #     logging.info(f"Error authenticating to Falcon API: {err}")
    #     log_http_error(response)
    #     raise
    # token = response.json()["access_token"]

    falcon = APIHarness(client_id=cs_client, client_secret=cs_secret,
                        base_url=cs_base_url, user_agent="zscaler-falcon-intel-bridge-v2.2")

    return falcon


def zs_auth():
    """Generates a new Zscaler API Auth Token, hot off the press
    returns: Zscaler API Auth token
    """
    logging.info(f"Authenticating to Zscaler API")
#    now = int(time.time() * 1000)
    url = f"{zs_vanity}/oauth2/v1/token"
    auth_string = f"{zs_client_id}:{zs_client_secret}" # mash id and secret
    auth_b64 = base64.b64encode(auth_string.encode()) # base64 encode
    auth_string = auth_b64.decode()
    payload = { "grant_type": "client_credentials",
        "audience": "https://api.zscaler.com"
             }
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': '*/*',
               'Authorization': 'Basic ' + auth_string
               }
 #   obfuscated_api_key = obfuscateApiKey(now)
 #   payload = {"username": zs_username, "password": zs_password,
 #              "apiKey": obfuscated_api_key, "timestamp": now}
 #   headers = {'Content-Type': 'application/json','cache-control': "no-cache"}
    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.info(f"Error authenticating to Zscaler API: {err}")
        log_http_error(response)
        raise
    js = response.json()
    token = js["access_token"]
#    token = response.cookies['JSESSIONID']
    return token
