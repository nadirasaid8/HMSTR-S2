import os
import json
import time
import requests
from colorama import *
from src.headers import get_headers
from src.deeplchain import read_config, log, mrh

init(autoreset=True)
config = read_config()
timeouts = config.get('LOOP_COUNTDOWN', 3800)

class oAuth:
    def __init__(self, token=None, account=None):
        self.base_url = 'https://api.hamsterkombatgame.io'
        self.headers = get_headers(token, account) if token else {}

    @staticmethod
    def local_token(account: str):
        if not os.path.exists("tokens.json"):
            with open("tokens.json", "w") as f:
                json.dump({}, f)
        with open("tokens.json") as f:
            return json.load(f).get(str(account))

    def save_token(self, account, token):
        try:
            with open("tokens.json", "r+") as f:
                tokens = json.load(f)
        except FileNotFoundError:
            tokens = {}
        tokens[str(account)] = token
        with open("tokens.json", "w") as f:
            json.dump(tokens, f, indent=4)

    def get_token(self, init_data, account, retries=5, backoff_factor=0.5, timeout=timeouts, proxies=None):
        url = f'{self.base_url}/auth/auth-by-telegram-webapp'
        headers = {
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Origin': 'https://hamsterkombatgame.io',
            'Referer': 'https://hamsterkombatgame.io/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12.0; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.8.5718.71 Mobile Safari/537.36',
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        data = json.dumps({"initDataRaw": init_data})

        for attempt in range(retries):
            try:
                res = requests.post(url, headers=headers, data=data, timeout=timeout, proxies=proxies)
                res.raise_for_status()
                response_data = res.json()

                token = response_data.get('authToken')
                if token:
                    self.save_token(account, token)
                    return token

                log(mrh + "No auth token found in the response.", flush=True)
                return None

            except (requests.ConnectionError, requests.Timeout) as e:
                log(mrh + f"Connection error on attempt {attempt + 1}: {e}", flush=True)
            except Exception as e:
                log(mrh + f"Failed to get token. Error: {e}", flush=True)
                try:
                    error_data = res.json()
                    if "invalid" in error_data.get("error_code", "").lower():
                        log(mrh + "Failed to get token. Invalid init data", flush=True)
                    else:
                        log(mrh + f"Failed to get token. {error_data}", flush=True)
                except Exception as json_error:
                    log(mrh + f"Failed to get token and unable to parse error response: {json_error}", flush=True)
                return None
            
            time.sleep(backoff_factor * (2 ** attempt))
        
        log(mrh + "Failed to get token after multiple attempts.", flush=True)
        return None

    def authenticate(self, token, account, proxies=None):
        self.headers = get_headers(token, account)
        url = f'{self.base_url}/auth/account-info'
        payload = {}
        
        try:
            res = requests.post(url, headers=self.headers, json=payload, proxies=proxies)
            res.raise_for_status()
        except Exception as e:
            log(mrh + f"Token Failed : {token[:4]}********* | Status : {res.status_code} | Error: {e}", flush=True)
            return None

        return res
