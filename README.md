# Hms Farming Bot 
This is a bot that can help you to run 'HMSTR Season 2' telegram bot!

[TELEGRAM CHANNEL](https://t.me/Deeplchain) | [TWITTER](https://x.com/itsjaw_real)

### This bot helpfull?  Please support me by buying me a coffee: 
```
0x705C71fc031B378586695c8f888231e9d24381b4 - EVM
TDTtTc4hSnK9ii1VDudZij8FVK2ZtwChja - TRON
UQBy7ICXV6qFGeFTRWSpnMtoH6agYF3PRa5nufcTr3GVOPri - TON
```

## Features
- Auto Sync = Claim profit per hour when idle
- Auto Buy Upgrade (with 4 method options) - `ON/OFF`
- Auto Buy Skin & Selected Highest Skin ID `Auto ON`
- Auto Complete Tasks - `ON/OFF`
- Static UserAgent - `Auto ON`
- Easily save and run your setup
- PROMO CODE & OTHER FEATURE COMING SOON!

##  Auto Upgrade metode
  1. Upgrade items with the **highest profit**
  2. Upgrade items at the **lowest price**
  3. Upgrade items with a **price less than balance**
  4. Upgrade item with the **highest payback** `RECOMENDED!`

## Prerequisites
Before installing and running this project, make sure you have the following prerequisites:
- Python 3.10+ (recomended)
- Other required dependencies

## Installation
1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/nadirasaid8/HMSTR-S2.git
    ```
2. Go to the project directory:
    ```bash
    cd HMSTR-S2
    ```
3. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
before starting the bot you must have your own initdata / queryid telegram!

1. Use PC/Laptop or Use USB Debugging Phone
2. open the `h*mst*r k*mb*t bot`
3. Inspect Element `(F12)` on the keyboard
4. at the top of the choose "`Application`" 
5. then select "`Session Storage`" 
6. Select the links "`H*mst*r Komb*t`" and "`tgWebAppData`"
7. Take the value part of "`tgWebAppData`"
8. take the part that looks like this: 

```txt 
query_id=xxxxxxxxx-Rxxxxuj&user=%7B%22id%22%3A1323733375%2C%22first_name%22%3A%22xxxx%22%2C%22last_name%22%3A%22%E7%9A%BF%20xxxxxx%22%2C%22username%22%3A%22xxxxx%22%2C%22language_code%22%3A%22id%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=xxxxx&hash=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
9. add it to `data.txt` file or create it if you dont have one


You can add more and run the accounts in turn by entering a query id in new line like this:
```txt
query_id=xxxxxxxxx-Rxxxxxxx&hash=xxxxxxxxxxx
query_id=xxxxxxxxx-Rxxxxxxx&hash=xxxxxxxxxxx
```

### Instant Setup:
- **Loading setup via CLI argument:** If the `--setup` argument is provided, the script will load the corresponding `.json` file and run the bot directly without displaying the menu.
- **Menu display:** If no `--setup` argument is provided, the script will display the menu as usual.
- **Setup saving:** The option to save setups has been included in the menu as option `8`.

This will allow you to run the script directly with a predefined setup like this:

```bash
python main.py --setup mysetup
```

### Add configuration setting on `config.json` 

 **bool** : `true` or `false`

  ```bash
{
    "use_proxy": false,
    "DELAY_UPGRADE": false,
    "MIN_DELAY_UPGRADE": 4,
    "MAX_DELAY_UPGRADE": 6,
    "DELAY_EACH_ACCOUNT": 5,
    "MAXIMUM_PRICE": 2,
    "LOOP_COUNTDOWN": 3800
}
  ```


### Create a `proxies.txt` file
The `proxies.txt` file should be in the root directory and contain a list of proxies in the format `username:password@host:port`.

Example:

```yaml
socks5://user1:pass1@ip1:port1
user2:pass2@ip2:port2
```

## RUN THE BOT
after that run the bot by writing the command

```bash
python main.py
```

## Can't Run this bot?
1. Add `皿 @Deeplchain` on your first or last name (not username)
2. Termux : `pip install requests colorama lxml requests-html`
3. Termux `lxml` issue : try `pip install lxml_html_clean` or `pip install lxml[html_clean]` or `pip install python-lxml`
4. Windows : `pip install requests colorama lxml-html-clean requests-html`

## License
This project is licensed under the `NONE` License.

## Contact
If you have any questions or suggestions, please feel free to contact us at [ https://t.me/DeeplChainSup ].

## Thanks to :

YOU 💘 (Full Source code by users of this scripts)


