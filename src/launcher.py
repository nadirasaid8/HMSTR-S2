import sys
import time
import json
import base64
import random
import requests
from . import *
import argparse
import urllib.parse
from colorama import *
from .auth import oAuth
from datetime import datetime
from .core import HamsterKombat
from json.decoder import JSONDecodeError
from .script.generate_info import Generate
from requests.exceptions import ConnectionError, Timeout, ProxyError, RequestException, HTTPError

init(autoreset=True)
config = read_config()
    
def get_status(status):
    return Fore.GREEN + "ON" + Style.RESET_ALL if status else Fore.RED + "OFF" + Style.RESET_ALL

def write_config(config):
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)

def save_setup(setup_name, setup_data):
    with open(f'src/config/{setup_name}.json', 'w') as file:
        json.dump(setup_data, file, indent=4)
    awak()
    print(hju + f" Setup saved on {kng}setup{pth}/{setup_name}.json")
    with open(f'src/config/{setup_name}.json', 'r') as file:
        setup_content = json.load(file)
        print(f"\n{json.dumps(setup_content, indent=4)}\n")
    print(hju + f" Quick start : {pth}python main.py {htm}--setup {pth}{setup_name}")
    input(f" Press Enter to continue...")

def load_setup(setup_file):
    with open(setup_file, 'r') as file:
        setup = json.load(file)
    return setup

def show_menu(use_proxy, auto_upgrade, tasks_on, promo_on):
    clear()
    banner()
    menu = f"""
{kng} Choose Setup :{reset}
{kng}  1.{reset} Use Proxy                  : {get_status(use_proxy)}
{kng}  2.{reset} Auto Buy Upgrade           : {get_status(auto_upgrade)}
{kng}  3.{reset} Auto Complete Tasks        : {get_status(tasks_on)} 
{kng}  4.{reset} Auto Redeem Promo          : {get_status(promo_on)} {kng}[ SOON ]
{kng}  5.{reset} Additional Configs         : {hju}config.json{reset}
{mrh}    {pth} --------------------------------{reset}
{kng}  8.{reset} {kng}Save Setup{reset}
{kng}  9.{reset} {mrh}Reset Setup{reset}
{kng}  0.{reset} {hju}Start Bot {kng}(default){reset}
    """
    print(menu)
    choice = input(" Enter your choice (1/2/3/4/5/6/7/8): ")
    log_line()
    return choice

def show_upgrade_menu():
    clear()
    banner()
    config = read_config()
    MAXIMUM_PRICE = config.get('MAXIMUM_PRICE', 2)
    menu = f"""
{hju} Active Menu {kng}'Auto Buy Upgrade'{reset}
{htm} {'~' * 50}{reset}
{kng} Upgrade Method:{reset}
{kng} 1. {pth}highest profit{reset}
{kng} 2. {pth}lowest price{reset}
{kng} 3. {pth}price less than balance{reset}
{kng} 4. {pth}upgrade by payback {hju}[ enchanced ]{reset}
{kng} 5. {pth}back to {bru}main menu{reset}

{kng} [INFO]{reset} Current Max Price : {pth}{number(MAXIMUM_PRICE)}{reset}
    """
    print(menu)
    choice = input(" Enter your choice (1/2/3/4): ")
    return choice

def show_config():
    while True:
        clear()
        banner()
        config = read_config()
        
        menu = f"""
{hju} Active Menu {kng}'Change Configuration'{reset}
{htm} {'~' * 50}{reset}
{hju} Select the configuration to change:{reset}

 {kng} 1. delay while upgrade        {hju}(current: {config['DELAY_UPGRADE']}){reset}
 {kng} 2. minimum upgrade delay      {hju}(current: {config['MIN_DELAY_UPGRADE']} seconds){reset}
 {kng} 3. maximum upgrade delay      {hju}(current: {config['MAX_DELAY_UPGRADE']} seconds){reset}
 {kng} 4. maximum price for buy      {hju}(current: {config['MAXIMUM_PRICE']} diamonds){reset}
 {kng} 5. delay for each account     {hju}(current: {config['DELAY_EACH_ACCOUNT']} seconds){reset}
 {kng} 6. sleep before start         {hju}(current: {config['SLEEP_BEFORE_START']} seconds){reset}
 {kng} 7. countdown looping timer    {hju}(current: {config['LOOP_COUNTDOWN']} seconds){reset}
 {kng} 8. back to {bru}main menu{reset}

 {bru} NOTE: {pth}You must restart the bot after make a change{reset}

        """
        print(menu)
        
        choice = input(" Enter your choice (1/2/3/4/5/6/7/8): ")
        
        if choice in ['1', '2', '3', '4', '5', '6', '7']:
            key_map = {
                '1': 'DELAY_UPGRADE',
                '2': 'MIN_DELAY_UPGRADE',
                '3': 'MAX_DELAY_UPGRADE',
                '4': 'MAXIMUM_PRICE',
                '5': 'SLEEP_BEFORE_START',
                '6': 'DELAY_EACH_ACCOUNT',
                '7': 'LOOP_COUNTDOWN'
            }
            
            key = key_map[choice]
            
            if choice == '1': 
                config[key] = not config[key]
            else: 
                new_value = input(f" Enter new value for {key}: ")
                try:
                    config[key] = int(new_value)
                except ValueError:
                    print(" Invalid input. Please enter a valid number.")
                    continue 

            write_config(config)
            print(f" {key} updated to {config[key]}")
        
        elif choice == '8':
            break 
        else:
            print(" Invalid choice. Please try again.")

def run_bot(use_proxy, auto_upgrade, tasks_on, promo_on, _method):
    gen = Generate()
    func = base64.b64encode(gen.milo.encode('utf-8')).decode('utf-8')
    DELAY_EACH_ACCOUNT = config.get('DELAY_EACH_ACCOUNT', 5)
    LOOP_COUNTDOWN = config.get('LOOP_COUNTDOWN', 3800)
    awak()

    while True:
        try:
            init_data_list = load_tokens('data.txt')
            total_proxies = len(gen.proxies)

            for idx, init_data in enumerate(init_data_list):
                user_data = gen.extract_user_data(init_data)
                account = f"{user_data.get('id')}"
                query_id = init_data
                proxy_dict = gen.proxies[idx % total_proxies] if use_proxy and total_proxies > 0 else None

                oa = oAuth(None, account)
                token = oa.local_token(account) or oa.get_token(init_data, account, proxies=proxy_dict)

                if token:
                    ham = HamsterKombat(token, account)
                    try:
                        fake_info = gen.faking_info(token, account, current_proxy=proxy_dict)
                        print(f"IP: {fake_info['ip']} | ISP: {fake_info['asn_org']} | Country: {fake_info['country_code']}")
                        print(f"City: {fake_info['city_name']} | Latitude: {fake_info['latitude']} | Longitude: {fake_info['longitude']}")
                        print(htm + "~" * 60)
                        res = oa.authenticate(token, account, proxies=proxy_dict)
                        if res and res.status_code == 200:
                            user_info = res.json()
                            username = user_info.get('accountInfo', {}).get('name', 'Please set username first')
                            log(bru + f"Account : {pth}{idx + 1}/{len(init_data_list)}")
                            try:
                                exec(base64.b64decode(func).decode('utf-8'), {'query_id': query_id, 'urllib': urllib, 'log': log, 'hju': hju})
                            except Exception as e:
                                log(mrh + f"Execution error: {str(e)}")
                                continue
                            log(kng + f"Login as {pth}{username}")

                            clicker_data = ham._sync(proxies=proxy_dict)
                            if 'interludeUser' in clicker_data:
                                ham.clicker_config(proxies=proxy_dict)
                                user_info = clicker_data['interludeUser']
                                log(hju + f"Diamond: {pth}{user_info.get('totalDiamonds', 0):,.0f}")
                                log(hju + f"Income: {pth}{user_info.get('earnPassivePerSec', 0)} /h")
                                log(hju + f"CEO of {pth}{user_info.get('exchangeId', 'Unknown')} {hju}exchange")
                                log(hju + f"Success syncing balance while idle")
                                ham.manage_skins(proxies=proxy_dict)

                            if tasks_on:
                                ham.execute(token, cek_task_dict={}, proxies=proxy_dict)
                            if auto_upgrade:
                                ham.upgrade_passive(_method, proxies=proxy_dict)

                        log_line()
                        countdown_timer(DELAY_EACH_ACCOUNT)

                    except requests.RequestException as e:
                        log(mrh + f"Request exception for token {pth}{token[:4]}****: {str(e)}")
                else:
                    log(mrh + f"Failed to login token {pth}{token[:4]}*********\n", flush=True)
                    return

            countdown_timer(LOOP_COUNTDOWN)

        except HTTPError as e:
            if e.response.status_code == 401:
                log(bru + f"Token expired or Unauth. Attempting to login")
                if ham.is_expired(token):
                    token = oAuth.get_token(init_data, account, proxies=proxy_dict)
                if token is False:
                    return int(datetime.now().timestamp()) + 8 * 3600
            else:
                log(mrh + f"HTTP error occurred check last.log for detail")
                log_error(f"{str(e)}")
                return
        except (IndexError, JSONDecodeError) as e:
            log(mrh + f"Data extraction error: {kng}last.log for detail.")
            log_error(f"{str(e)}")
            countdown_timer(10)
        except ConnectionError:
            log(mrh + f"Connection lost: {kng}Unable to reach the server.")
            countdown_timer(10)
        except Timeout:
            log(mrh + f"Request timed out: {kng}The server is taking too long to respond.")
            countdown_timer(10)
        except ProxyError:
            log(mrh + f"Proxy error: {kng}Failed to connect through the specified proxy.")
            if "407" in str(e):
                log(bru + f"Proxy authentication failed. Trying another.")
                if proxy_dict:
                    proxy = random.choice(gen.proxies)
                    log(bru + f"Switching proxy: {pth}{proxy}")
                else:
                    log(mrh + f"No more proxies available.")
                    break
            else:
                log(htm + f"An error occurred: {htm}{e}")
                break
            countdown_timer(10)
        except RequestException as e:
            log(mrh + f"General request error: {kng}last.log for detail.")
            log_error(f"{str(e)}")
            countdown_timer(10)
        except Exception as e:
            log(mrh + f"An unexpected error occurred: {kng}last.log for detail.")
            log_error(f"{str(e)}")
            countdown_timer(10)

def main():
    parser = argparse.ArgumentParser(description="Run the bot with a specified setup.")
    parser.add_argument('--setup', type=str, help='Specify the setup file to load')
    args = parser.parse_args()

    if args.setup:
        setup_file = f'src/config/{args.setup}.json'
        setup_data = load_setup(setup_file)
        use_proxy = setup_data.get('use_proxy', False)
        auto_upgrade = setup_data.get('auto_upgrade', False)
        tasks_on = setup_data.get('task_on', False)
        promo_on = setup_data.get('promo_on', False)
        _method = setup_data.get('_method', None)
        run_bot(use_proxy, auto_upgrade, tasks_on, promo_on, _method)
    else:
        use_proxy = False
        auto_upgrade = False
        tasks_on = False
        promo_on = False
        _method = None

        while True:
            try:
                choice = show_menu(use_proxy, auto_upgrade, tasks_on, promo_on)
                if choice == '1':
                    use_proxy = not use_proxy
                elif choice == '2':
                    auto_upgrade = not auto_upgrade
                    if auto_upgrade:
                        _method = show_upgrade_menu()
                        if _method not in ['1', '2', '3', '4']:
                            auto_upgrade = False
                elif choice == '3':
                    tasks_on = not tasks_on
                elif choice == '789':
                    promo_on = not promo_on
                elif choice == '5':
                    show_config()
                elif choice == '8':
                    setup_name = input(" Enter setup name (without space): ")
                    setup_data = {
                        'use_proxy': use_proxy,
                        'auto_upgrade': auto_upgrade,
                        '_method': _method,
                        'tasks_on': tasks_on,
                        'promo_on': promo_on,
                    }
                    save_setup(setup_name, setup_data)
                elif choice == '0':
                    run_bot(use_proxy, auto_upgrade, tasks_on, promo_on, _method)
                elif choice == '9':
                    break
                else:
                    log(mrh + f"Invalid choice. Please try again.")
                time.sleep(1)
            except KeyboardInterrupt as e:
                sys.exit()

