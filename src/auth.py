import json
import time
import requests
from colorama import *
from src.headers import get_headers
from src.script.generate_ua import get_user_agent
from src.deeplchain import read_config, log, mrh

init(autoreset=True)
config = read_config()
timeouts = config.get('LOOP_COUNTDOWN', 3800)

def get_token(init_data_raw, account, retries=5, backoff_factor=0.5, timeout=timeouts, proxies=None):
    url = 'https://api.hamsterkombatgame.io/auth/auth-by-telegram-webapp'
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombatgame.io',
        'Referer': 'https://hamsterkombatgame.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': get_user_agent(account),
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    data = json.dumps({"initDataRaw": init_data_raw})

    for attempt in range(retries):
        try:
            res = requests.post(url, headers=headers, data=data, timeout=timeout, proxies=proxies)
            res.raise_for_status()
            return res.json()['authToken']
        except (requests.ConnectionError, requests.Timeout) as e:
            log(mrh + f"Connection error on attempt {attempt + 1}: {e}", flush=True)
        except Exception as e:
            log(mrh + f"Failed Get Token. Error: {e}", flush=True)
            try:
                error_data = res.json()
                if "invalid" in error_data.get("error_code", "").lower():
                    log(mrh + "Failed Get Token. Invalid init data", flush=True)
                else:
                    log(mrh + f"Failed Get Token. {error_data}", flush=True)
            except Exception as json_error:
                log(mrh + f"Failed Get Token and unable to parse error response: {json_error}", flush=True)
            return None
        time.sleep(backoff_factor * (2 ** attempt))
    log(mrh + "Failed to get token after multiple attempts.", flush=True)
    return None

def authenticate(token, account, proxies=None):
    url = 'https://api.hamsterkombatgame.io/auth/account-info'
    headers = get_headers(token, account)
    payload = {}
    
    try:
        res = requests.post(url, headers=headers, json=payload, proxies=proxies)
        res.raise_for_status()
    except Exception as e:
        log(mrh + f"Token Failed : {token[:4]}********* | Status : {res.status_code} | Error: {e}", flush=True)
        return None

    return res