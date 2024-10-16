import os
import json
import time
from datetime import datetime
from colorama import *

mrh = Fore.LIGHTRED_EX
pth = Fore.LIGHTWHITE_EX
hju = Fore.LIGHTGREEN_EX
kng = Fore.LIGHTYELLOW_EX
bru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL
htm = Fore.LIGHTBLACK_EX

last_log_message = None

def banner():
    banner = r"""
 ██╗████████╗███████╗     ██╗ █████╗ ██╗    ██╗
 ██║╚══██╔══╝██╔════╝     ██║██╔══██╗██║    ██║
 ██║   ██║   ███████╗     ██║███████║██║ █╗ ██║
 ██║   ██║   ╚════██║██   ██║██╔══██║██║███╗██║
 ██║   ██║   ███████║╚█████╔╝██║  ██║╚███╔███╔╝
 ╚═╝   ╚═╝   ╚══════╝ ╚════╝ ╚═╝  ╚═╝ ╚══╝╚══╝  """ 
    print(Fore.GREEN + Style.BRIGHT + banner + Style.RESET_ALL)
    print(hju + f" H*mst*r K*mb*t Season 2")
    print(mrh + f" FREE TO USE = Join us on {pth}@DEEPLCHAIN")
    print(mrh + f" before start please '{hju}git pull{mrh}' to update bot")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def read_config():
    config_path = os.path.join(os.path.dirname(__file__), '../config.json')
    with open(config_path, 'r') as file:
        try:
            config_content = file.read()
            return json.loads(config_content)
        except json.JSONDecodeError as e:
            return {}
        
def log(message, **kwargs):
    global last_log_message
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    flush = kwargs.pop('flush', False)
    end = kwargs.pop('end', '\n')
    if message != last_log_message:
        print(f"{htm}[{current_time}] {message}", flush=flush, end=end)
        last_log_message = message

def log_error(message):
    with open('last.log', 'a') as log_file:
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ERROR - {message}\n")


def log_line():
    print(pth + "~" * 60)

def awak():
    clear()
    banner()
    log_line()

def countdown_timer(seconds):
    while seconds:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        h = str(h).zfill(2)
        m = str(m).zfill(2)
        s = str(s).zfill(2)
        print(f"{pth}please wait until {h}:{m}:{s} ", flush=True, end="\r")
        seconds -= 1
        time.sleep(1)
    print(f"{pth}please wait until {h}:{m}:{s} ", flush=True, end="\r")

def number(number):
    return "{:,.0f}".format(number)

def load_tokens(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []