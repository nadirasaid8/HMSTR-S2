import sys

from src.core import main
from src.deeplchain import banner, log, mrh

if __name__ == "__main__":
    while True:
        try:
            banner()
            main()
        except KeyboardInterrupt:
            print()
            log(mrh + f"Successfully logged out of the bot\n")
            sys.exit()
