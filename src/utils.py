import json
import time
import random
from random import randint
import requests
from datetime import datetime
from colorama import *
from src.headers import get_headers
from . import *

config = read_config()

class HamsterKombat:
    def __init__(self, token, account):
        self.headers = get_headers(token, account)
        self.base_url = f"https://api.hamsterkombatgame.io"

    def clicker_config(self, proxies=None):
        url = f'{self.base_url}/interlude/config'
        try:
            response = requests.post(url, headers=self.headers, proxies=proxies)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to retrieve config, status code: {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def _sync(self, proxies=None):
        url = f'{self.base_url}/interlude/sync'
        try:
            response = requests.post(url, headers=self.headers, proxies=proxies)
            if response.status_code == 200:
                return response.json()
            else:
                return {}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        
    def manage_skins(self, proxies=None):
        sync_data = self._sync(proxies)
        available_skins = sync_data.get('interludeUser', {}).get('skin', {}).get('available', [])
        selected_skin = sync_data.get('interludeUser', {}).get('skin', {}).get('selectedSkinId', None)

        url = f'{self.base_url}/interlude/get-skin'
        try:
            response = requests.post(url, headers=self.headers, proxies=proxies)
            if response.status_code == 200:
                skins = response.json().get('skins', [])
            else:
                return
        except requests.exceptions.RequestException as e:
            log(f"Error fetching skins: {e}")
            return

        max_skin_id = None
        for skin in skins:
            if skin['isAvailable'] and not skin['isExpired']:
                skin_id = skin['id']
                if skin_id not in [s['skinId'] for s in available_skins]:
                    payload = {"skinId": skin_id, "timestamp": int(datetime.now().timestamp())}
                    buy_url = f'{self.base_url}/interlude/buy-skin'
                    buy_response = requests.post(buy_url, headers=self.headers, json=payload, proxies=proxies)
                    if buy_response.status_code == 200:
                        log(hju + f"Successfully bought {skin_id}")
                        rentime = random.uniform(1, 2.1)
                        time.sleep(rentime)

                if max_skin_id is None or int(skin_id.replace('skin', '')) > int(max_skin_id.replace('skin', '')):
                    max_skin_id = skin_id

        if max_skin_id and max_skin_id != selected_skin:
            payload = {"skinId": max_skin_id}
            select_url = f'{self.base_url}/interlude/select-skin'
            select_response = requests.post(select_url, headers=self.headers, json=payload, proxies=proxies)
            if select_response.status_code == 200:
                log(hju + f"Successfully selected {max_skin_id}")
        else:
            log(hju + "Already selected highest skin id")

    def exchange(self, proxies=None):
        url = f'{self.base_url}/interlude/select-exchange'
        choose = random.choice(['okx', 'bybit', 'binance', 'bingx'])  # Use parentheses for choice
        payload = {
            "exchangeId": choose
        }
        try:
            response = requests.post(url, headers=self.headers, json=payload, proxies=proxies)
            if response.status_code == 200:
                log(hju + f"Choose {choose} exchanged successfully")
            else:
                log(mrh + "Failed to choose exchange")
        except Exception as e:
            log(mrh + f"Error exchanging token: {e}")

    def execute(self, token, cek_task_dict, proxies: None):
        if token not in cek_task_dict:
            cek_task_dict[token] = False
        
        if not cek_task_dict[token]:
            list_url = f'{self.base_url}/interlude/list-tasks'
            list_res = requests.post(list_url, headers=self.headers, proxies=proxies)

            if list_res.status_code == 200:
                tasks = list_res.json().get('tasks', [])
                all_completed = all(task['isCompleted'] or task['id'] == 'invite_friends' for task in tasks)

                if all_completed:
                    log(f"{kng}All tasks have been claimed successfully\r", flush=True)
                else:
                    for task in tasks:
                        if not task['isCompleted']:
                            check_url = f'{self.base_url}/interlude/check-task'
                            data = json.dumps({"taskId": task['id']})
                            check_res = requests.post(check_url, headers=self.headers, data=data, proxies=proxies)

                            if check_res.status_code == 200 and check_res.json()['task']['isCompleted']:
                                log(f"{hju}Task {pth}{task['id']} {hju}success\r", flush=True)
                                countdown_timer(3)
                            else:
                                log(f"{hju}Task {mrh}failed {pth}{task['id']}\r", flush=True)
                cek_task_dict[token] = True
            else:
                log(f"{hju}Failed to get task list {pth}{list_res.status_code}\r", flush=True)

    def upgrade_passive(self, _method, proxies: None):
        MAXIMUM_PRICE = config.get('MAXIMUM_PRICE', 2)

        clicker_data = self._sync(proxies)
        if 'interludeUser' in clicker_data:
            user_info = clicker_data['interludeUser']
            balance_coins = user_info['balanceDiamonds']
        else:
            log(mrh + f"Failed to get user data\r", flush=True)
            return

        upgrades = self.available_upgrades(proxies)
        if not upgrades:
            log(mrh + f"\rFailed to get data or no upgrades available\r", flush=True)
            return

        log(bru + f"Total card available: {pth}{len(upgrades)}", flush=True)

        if _method == '1':
            upg_sort = sorted(
                [u for u in upgrades if u['price'] <= MAXIMUM_PRICE and u['price'] > 0],
                key=lambda x: -x['profitPerHour'] / x['price'] if x['price'] > 0 else 0,
                reverse=False
            )
        elif _method == '2':
            upg_sort = sorted(
                [u for u in upgrades if u['price'] <= MAXIMUM_PRICE and u['profitPerHour'] > 0 and u.get("price", 0) > 0],
                key=lambda x: x['price'] / x["profitPerHour"] if x['profitPerHour'] > 0 else float('inf'),
                reverse=False
            )
        elif _method == '4':
            upg_sort = sorted(
                [u for u in upgrades if u['price'] <= MAXIMUM_PRICE and u['price'] > 0 and u.get("profitPerHour", 0) > 0],
                key=lambda x: x["profitPerHour"] / x["price"] if x['profitPerHour'] > 0 else float('inf'),
                reverse=True
            )
        elif _method == '3':
            upg_sort = [u for u in upgrades if u['price'] <= balance_coins and u['price'] <= MAXIMUM_PRICE]
            if not upg_sort:
                log(mrh + f"No upgrade available less than balance\r", flush=True)
                return
        else:
            log(mrh + "Invalid option, please try again", flush=True)
            return

        if not upg_sort:
            log(bru + f"No {pth}item {bru}available under {pth}{number(MAXIMUM_PRICE)}\r", flush=True)
            return

        any_upgrade_attempted = False
        upgrades_purchased = False
        while True:
            for upgrade in upg_sort:
                if upgrade['isAvailable'] and not upgrade['isExpired']:
                    status = self.buy_upgrade(
                        upgrade['id'], 
                        upgrade['name'], 
                        upgrade['level'], 
                        upgrade['profitPerHour'], 
                        upgrade['price'],
                        proxies
                    )
                    
                    if status == 'insufficient_funds':
                        clicker_data = self._sync(proxies)
                        if 'interludeUser' in clicker_data:
                            user_info = clicker_data['interludeUser']
                            balance_coins = user_info['balanceDiamonds']
                            log(mrh + f"Balance after : {pth}{number(balance_coins)}")
                        return
                    elif status == 'success':
                        upgrades_purchased = True
                        continue
                    else:
                        continue
            
            if not any_upgrade_attempted:
                log(bru + f"No {pth}item {bru}available under {pth}{number(MAXIMUM_PRICE)}\r", flush=True)
                break
            elif not upgrades_purchased:
                any_upgrade_attempted = True

    def available_upgrades(self, proxies=None):
        url = f'{self.base_url}/interlude/upgrades-for-buy'
        res = requests.post(url, headers=self.headers, proxies=proxies)
        if res.status_code == 200:
            return res.json()['upgradesForBuy']
        else:
            log(mrh + f"Failed to get upgrade list: {res.json()}\r", flush=True)
            return []

    def buy_upgrade(self, upgrade_id: str, upgrade_name: str, level: int, profitPerHour: float, price: float, proxies=None) -> str:
        url = f'{self.base_url}/interlude/buy-upgrade'
        data = json.dumps({"upgradeId": upgrade_id, "timestamp": int(time.time())})
        res = requests.post(url, headers=self.headers, data=data, proxies=proxies)
        DELAY_UPGRADE = config.get('DELAY_UPGRADE', False)
        MIN_DELAY_UPGRADE = config.get('MIN_DELAY_UPGRADE',0)
        MAX_DELAY_UPGRADE = config.get('MAX_DELAY_UPGRADE',1)
        log(bru + f"Card {hju}name {pth}{upgrade_name}    \r", flush=True)
        log(bru + f"Card {hju}price{pth} {number(price)}       \r", flush=True)
        
        if res.status_code == 200:
            log(hju + f"Success {bru}| Level {pth}+{level} | +{kng}{profitPerHour}{pth}/h         \r", flush=True)
            if DELAY_UPGRADE:
                countdown_timer(randint(MIN_DELAY_UPGRADE, MAX_DELAY_UPGRADE))
            else:
                time.sleep(0.3)
            return 'success'
        else:
            error_res = res.json()
            if error_res.get('error_code') == 'INSUFFICIENT_FUNDS':
                log(mrh + f"Insufficient {kng}funds for this card       ", flush=True)
                return 'insufficient_funds'
            elif error_res.get('error_code') == 'UPGRADE_COOLDOWN':
                cooldown_time = error_res.get('cooldownSeconds')
                log(bru + f"Card {kng}cooldown for {pth}{cooldown_time} {kng}seconds.       ", flush=True)
                return 'cooldown'
            elif error_res.get('error_code') == 'UPGRADE_MAX_LEVEL':
                log(bru + f"Card {kng}is already on max level  ", flush=True)
                return 'max_level'
            elif error_res.get('error_code') == 'UPGRADE_NOT_AVAILABLE':
                log(bru + f"Not Meet{mrh} requirements to buy card", flush=True)
                return 'not_available'
            elif error_res.get('error_code') == 'UPGRADE_HAS_EXPIRED':
                log(bru + f"Card {kng}has expired you'are late      ", flush=True)
                return 'expired'
            elif error_res.get('error_code') == 'EXCHANGE_NOT_SELECTED':
                log(bru + f"To upgrade you need to select an exchange", flush=True)
                self.exchange(proxies)
            else:
                log(kng + f"{res.json()}       ", flush=True)
                return 'error'
