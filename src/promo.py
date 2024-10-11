import requests
from collections import defaultdict
from src.headers import get_headers
from src.deeplchain import countdown_timer, log, hju, kng, mrh, pth, bru

def load_promo(filename='./data/promo.txt'):
    with open(filename, 'r') as file:
        promo_codes = [line.strip() for line in file]
    promo_dict = defaultdict(list)
    for code in promo_codes:
        code_type = code.split('-')[0]
        promo_dict[code_type].append(code)
    return promo_dict

def save_promo(promo_dict, filename='./data/promo.txt'):
    with open(filename, 'w') as file:
        for code_list in promo_dict.values():
            for code in code_list:
                file.write(code + '\n')

def redeem_promo(token):
    promo_dict = load_promo()

    if not promo_dict:
        log(mrh + f"No codes available in {pth}promo.txt.")
        return

    max_attempts = 4
    attempts_tracker = defaultdict(int)
    http_error_tracker = defaultdict(int)
    max_http_errors = 2

    while promo_dict:
        for code_type, codes in list(promo_dict.items()):
            if attempts_tracker[code_type] >= max_attempts:
                if codes:
                    log(hju + f"4/4 {pth}{code_type} {kng}have been applied today.")
                continue

            promo_code = codes[0]
            url = 'https://api.hamsterkombatgame.io/clicker/apply-promo'
            headers = get_headers(token)
            payload = {"promoCode": promo_code}

            try:
                res = requests.post(url, headers=headers, json=payload)
                res.raise_for_status()

                if res.status_code == 200:
                    log(hju + f"Applied Promo {pth}{promo_code}")
                    codes.pop(0)
                    save_promo(promo_dict)
                    countdown_timer(5)
                    attempts_tracker[code_type] += 1
                    http_error_tracker[code_type] = 0 
                else:
                    log(kng + f"Failed to apply {pth}{promo_code}")
                    codes.pop(0)
                    save_promo(promo_dict)

            except requests.exceptions.HTTPError as e:
                try:
                    error_data = res.json()
                    if error_data.get('error_code') == "MaxKeysReceived":
                        log(pth + f"{code_type} {hju}Max keys received for today.")
                        attempts_tracker[code_type] = max_attempts
                    else:
                        log(kng + f"Error applying {pth}{promo_code}: {error_data.get('error_message')}")
                        http_error_tracker[code_type] += 1
                        if http_error_tracker[code_type] >= max_http_errors:
                            log(pth + f"{code_type} {hju}Assuming maximum redemption")
                            codes.pop(0)
                            save_promo(promo_dict)
                            attempts_tracker[code_type] = max_attempts
                except ValueError:
                    log(kng + f"Error applying {pth}{promo_code}")
                    http_error_tracker[code_type] += 1
                    if http_error_tracker[code_type] >= max_http_errors:
                        log(pth + f"{code_type} {hju}Assuming maximum redemption")
                        codes.pop(0)
                        save_promo(promo_dict)
                        attempts_tracker[code_type] = max_attempts

            except Exception as err:
                log(mrh + f"Error: {err}. Promo code: {promo_code}")
                codes.pop(0)  
                save_promo(promo_dict)

        if all(attempts >= max_attempts or not codes for attempts, codes in zip(attempts_tracker.values(), promo_dict.values())):
            break

    if all(attempts >= max_attempts for attempts in attempts_tracker.values()):
        log(bru + "Max reached for all promo types.")
