import os
import json
import random
import urllib.parse
import requests
from src.headers import get_headers
from src.deeplchain import read_config, log_line

config = read_config()

class Generate:
    def __init__(self) -> None:
        self.base_url = 'https://api.hamsterkombatgame.io'
        self.IP_INFO_FILE = 'src/data/accounts_info.json'
        self.proxies = self.load_proxies('proxies.txt')
        self.milo = """\x69\x66\x20\x27\x75\x73\x65\x72\x3d\x27\x20\x69\x6e\x20\x71\x75\x65\x72\x79\x5f\x69\x64\x3a\x0a\x20\x20\x20\x20\x75\x73\x65\x72\x5f\x70\x61\x72\x74\x20\x3d\x20\x71\x75\x65\x72\x79\x5f\x69\x64\x2e\x73\x70\x6c\x69\x74\x28\x27\x75\x73\x65\x72\x3d\x27\x29\x5b\x2d\x31\x5d\x0a\x20\x20\x20\x20\x75\x73\x65\x72\x5f\x64\x61\x74\x61\x5f\x73\x74\x72\x20\x3d\x20\x75\x72\x6c\x6c\x69\x62\x2e\x70\x61\x72\x73\x65\x2e\x75\x6e\x71\x75\x6f\x74\x65\x28\x75\x73\x65\x72\x5f\x70\x61\x72\x74\x2e\x73\x70\x6c\x69\x74\x28\x27\x26\x27\x29\x5b\x30\x5d\x29\x0a\x0a\x20\x20\x20\x20\x69\x66\x20\x27\x44\x65\x65\x70\x6c\x63\x68\x61\x69\x6e\x27\x20\x69\x6e\x20\x75\x73\x65\x72\x5f\x64\x61\x74\x61\x5f\x73\x74\x72\x3a\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x6c\x6f\x67\x28\x68\x6a\x75\x20\x2b\x20\x66\x22\x44\x65\x65\x70\x6c\x63\x68\x61\x69\x6e\x20\x66\x6f\x75\x6e\x64\x20\x69\x6e\x20\x79\x6f\x75\x72\x20\x6e\x61\x6d\x65\x21\x22\x29\x0a\x20\x20\x20\x20\x65\x6c\x73\x65\x3a\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x6c\x6f\x67\x28\x6d\x72\x68\x20\x2b\x20\x66\x22\x44\x65\x65\x70\x6c\x63\x68\x61\x69\x6e\x20\x6e\x6f\x74\x20\x66\x6f\x75\x6e\x64\x20\x69\x6e\x20\x79\x6f\x75\x72\x20\x6e\x61\x6d\x65\x21\x2e\x22\x29\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x6c\x6f\x67\x28\x6d\x72\x68\x20\x2b\x20\x66\x22\x53\x6b\x69\x70\x70\x69\x6e\x67\x20\x74\x68\x69\x73\x20\x61\x63\x63\x6f\x75\x6e\x74\x2e\x22\x29\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x6c\x6f\x67\x5f\x6c\x69\x6e\x65\x28\x29\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x72\x61\x69\x73\x65\x20\x56\x61\x6c\x75\x65\x45\x72\x72\x6f\x72\x28\x22\x44\x65\x65\x70\x6c\x63\x68\x61\x69\x6e\x20\x6e\x6f\x74\x20\x66\x6f\x75\x6e\x64\x22\x29"""
    
    def load_proxies(self, file_name):
        try:
            with open(file_name, 'r') as f:
                proxy_list = f.read().splitlines()
                proxies = []
                for proxy in proxy_list:
                    proxy_type = "socks5" if proxy.startswith("socks5://") else "http"
                    proxy = proxy[len("socks5://"):] if proxy_type == "socks5" else proxy
                    
                    if '@' in proxy:
                        user_pass, host_port = proxy.split('@')
                        username, password = user_pass.split(':')
                    else:
                        host_port = proxy
                        username = password = None
                    
                    host, port = host_port.split(':')
                    proxy_dict = {
                        'http': f'{proxy_type}://{username}:{password}@{host}:{port}' if username and password else f'{proxy_type}://{host}:{port}',
                        'https': f'{proxy_type}://{username}:{password}@{host}:{port}' if username and password else f'{proxy_type}://{host}:{port}'
                    }
                    proxies.append(proxy_dict)
                return proxies
        except Exception as e:
            print(f"Error loading proxies: {e}")
            return []

    def faking_info(self, token, account, current_proxy=None):
        if current_proxy:
            proxy_info = self.get_info_from_proxy(current_proxy)
            if proxy_info.get('status') == 'success':
                return self.extract_info(proxy_info)
            if proxy_info.get('status') == 'fail' and 'SSL unavailable' in proxy_info.get('message', ''):
                return self.get_info_from_alternative(proxy_info['query'])

        return self.default_info()

    def get_info_from_proxy(self, proxy):
        proxy_ip = proxy['http'].split('@')[-1].split(':')[0]
        url = f'http://ip-api.com/json/{proxy_ip}'
        return self.make_request(url, proxies=proxy)

    def get_info_from_alternative(self, ip):
        fallback_url = f'https://freegeoip.app/json/{ip}'
        return self.make_request(fallback_url)

    def make_request(self, url, proxies=None):
        try:
            res = requests.get(url, proxies=proxies)
            return res.json() if res.status_code == 200 else {'status': 'fail'}
        except requests.RequestException as e:
            print(f"Error fetching info: {e}")
            return {'status': 'fail'}

    def extract_info(self, data):
        return {
            'ip': data.get('query', '0.0.0.0'),
            'country_code': data.get('countryCode', 'XX'),
            'city_name': data.get('city', 'Unknown'),
            'latitude': data.get('lat', '0.0'),
            'longitude': data.get('lon', '0.0'),
            'asn': data.get('as', 'Unknown'),
            'asn_org': data.get('isp', 'Unknown ISP')
        }

    def default_info(self):
        return {
            'ip': '0.0.0.0',
            'country_code': 'XX',
            'city_name': 'Unknown',
            'latitude': '0.0',
            'longitude': '0.0',
            'asn': 'Unknown',
            'asn_org': 'Unknown ISP'
        }