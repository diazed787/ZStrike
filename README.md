# ZIA/Falcon Integration: The Intel Bridge

This tool seamlessly integrates CrowdStrike's Falcon's Threat Intelligence with Zscaler's Zero Trust Exchange to provide an extra layer of security and visibility for web access. CrowdStrike's Falcon Intel module includes access to  cutting edge database of Indicators of Compromise curated by intelligence experts. 

During runtime, the integration maintains a custom URL category in Zscaler Internet Access. Left to run indefinitely and unsupervised, it will automatically populate its URL Category with the newest Falcon Intel Indicators. This occurs in a 12 hour loop, and can be left running on a server for eternity or scheduled as a chron job.

# Getting Started
First, remove any CrowdStrike related URL Categories from your ZIA tenant from previous iterations of the integration. You only need to do this once, the script handles its creation and maintenence.
## Requirements
- zscaler ZIA
- CrowdStrike Falcon Intel
- Python 3+ (Python 2 will not work due to string parsing incompatibilities)

[zscaler URL Category documentation](https://help.zscaler.com/zia/adding-custom-url-categories)

## CrowdStrike OAuth2 Token Scope
In the Falcon UI, navigate to API Clients and Keys. Then, click Add a New API Client. Create a client with READ permissions for Indicators (Falcon Intel). Save the resulting values, as you will need them to run the integration.

## Download Repository
```bash
git clone https://github.com/diazed787/ZStrike.git
cd ZStrike
```

## Install Dependencies with pip3
```bash
pip3 install -r requirements.txt
```
## Rename Sample INI File
```bash
mv config.ini.example config.ini
```
## Configure
Input your configurations in config.ini. Do not use quotes or ticks for any of these values.

Most of the fields are self-explanatory, but be sure to put some thought into the LIMIT field. This field determines how many malicious URLs the Intel Bridge will maintain in your ZIA tenant. Zscaler offers different subscription tiers with varying maximum custom URLs (from 25K to 275K). Consider this, as well as your existing custom URL categories when you choose a value, as going over the limit will cause runtime errors. So for example, if you have a limit of 25K, and are already using 10K in another URL category, consider a value like 14000. That way, you won't go over the limit, and you leave yourself some wiggle room.


```ini
[CROWDSTRIKE]
client=
secret=
base_url=https://api.us-2.crowdstrike.com
type=url
limit=10000

# ZScaler configurations
[ZSCALER]
auth_hostname=https://<vanity_url>.zslogin.net
client_id=
client_secret=
hostname=https://api.zsapi.net/zia/api/v1

#If running as a chron job, set this value to 1
#When disable_loop=1, the script will exit after completing a cycle
[CHRON]
disable_loop=0

#When log_indicators=1, indicators will be logged in logs/data_log as they are deleted and loaded.
[LOG]
log_indicators=0
```
# Running the Integration
With Python 3.7+ installed:
```bash
python3 intelbridge
```
