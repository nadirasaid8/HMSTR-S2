from .script.generate_ua import get_user_agent

def get_headers(token: str, account) -> dict:
    return {
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'content-type':'application/json',
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombatgame.io',
        'Referer': 'https://hamsterkombatgame.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': get_user_agent(account),
        'Content-Type': 'application/json'
    }

def load_tokens(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []
