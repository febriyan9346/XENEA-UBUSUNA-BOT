import os
import time
import random
import sys
import itertools
from datetime import datetime
import pytz
from colorama import Fore, Style, init
from web3 import Web3
from eth_account import Account
import warnings

os.system('clear' if os.name == 'posix' else 'cls')

warnings.filterwarnings('ignore')
if not sys.warnoptions:
    os.environ["PYTHONWARNINGS"] = "ignore"

init(autoreset=True)
Account.enable_unaudited_hdwallet_features()

class XeneaBot:
    def __init__(self):
        self.rpc_url = "https://rpc-ubusuna.xeneascan.com"
        self.chain_id = 1096
        self.symbol = "TXENE"
        self.explorer_url = "https://xeneascan.com/tx"

    def get_wib_time(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib).strftime('%H:%M:%S')

    def print_banner(self):
        banner = f"""
{Fore.CYAN}XENEA UBUSUNA BOT{Style.RESET_ALL}
{Fore.WHITE}By: FEBRIYAN{Style.RESET_ALL}
{Fore.CYAN}============================================================{Style.RESET_ALL}
"""
        print(banner)

    def log(self, message, level="INFO"):
        time_str = self.get_wib_time()

        if level == "INFO":
            color = Fore.CYAN
            symbol = "[INFO]"
        elif level == "SUCCESS":
            color = Fore.GREEN
            symbol = "[SUCCESS]"
        elif level == "ERROR":
            color = Fore.RED
            symbol = "[ERROR]"
        elif level == "WARNING":
            color = Fore.YELLOW
            symbol = "[WARNING]"
        elif level == "CYCLE":
            color = Fore.MAGENTA
            symbol = "[CYCLE]"
        else:
            color = Fore.WHITE
            symbol = "[LOG]"

        print(f"[{time_str}] {color}{symbol} {message}{Style.RESET_ALL}")

    def random_delay(self, min_sec=3, max_sec=10):
        delay = random.randint(min_sec, max_sec)
        self.log(f"Delay {delay} seconds...", "INFO")
        time.sleep(delay)

    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            print(f"\r[COUNTDOWN] Next cycle in: {hours:02d}:{minutes:02d}:{secs:02d} ", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 60 + "\r", end="", flush=True)

    def get_proxies(self):
        proxies = []
        try:
            with open('proxy.txt', 'r') as file:
                for line in file:
                    p = line.strip()
                    if p:
                        if not p.startswith('http'):
                            p = f"http://{p}"
                        proxies.append(p)
        except FileNotFoundError:
            pass
        return proxies

    def get_random_address(self):
        return Account.create().address

    def show_proxy_menu(self):
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Select Proxy Mode:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Run with proxy")
        print(f"2. Run without proxy{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        while True:
            try:
                choice = input(f"{Fore.GREEN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
                if choice in ['1', '2']:
                    return choice
                print(f"{Fore.RED}Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Program terminated by user.{Style.RESET_ALL}")
                exit(0)

    def show_target_menu(self):
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Select Destination:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Load from address.txt")
        print(f"2. Random Address{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        while True:
            try:
                choice = input(f"{Fore.GREEN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
                if choice in ['1', '2']:
                    return choice
                print(f"{Fore.RED}Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Program terminated by user.{Style.RESET_ALL}")
                exit(0)

    def run(self):
        self.print_banner()

        proxy_choice = self.show_proxy_menu()
        target_choice = self.show_target_menu()

        try:
            amount_str = input(f"{Fore.GREEN}Enter Transfer Amount ({self.symbol}): {Style.RESET_ALL}").strip()
            amount_to_send = float(amount_str)
            tx_count_str = input(f"{Fore.GREEN}Enter TX Count per Account: {Style.RESET_ALL}").strip()
            tx_count = int(tx_count_str)
        except ValueError:
            self.log("Invalid input. Must be a number.", "ERROR")
            sys.exit()
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Program terminated by user.{Style.RESET_ALL}")
            exit(0)

        print(f"\n{Fore.CYAN}============================================================{Style.RESET_ALL}\n")

        cycle = 1
        while True:
            self.log(f"Cycle #{cycle} Started", "CYCLE")
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")

            try:
                with open('accounts.txt', 'r') as file:
                    private_keys = [line.strip() for line in file if line.strip()]
            except FileNotFoundError:
                self.log("accounts.txt not found!", "ERROR")
                sys.exit()

            if not private_keys:
                self.log("accounts.txt is empty!", "ERROR")
                sys.exit()

            target_addresses = []
            if target_choice == '1':
                try:
                    with open('address.txt', 'r') as file:
                        target_addresses = [line.strip() for line in file if line.strip()]
                except FileNotFoundError:
                    self.log("address.txt not found, fallback to random", "WARNING")
                    target_choice = '2'

            proxies = []
            if proxy_choice == '1':
                proxies = self.get_proxies()
                self.log(f"Running with proxy ({len(proxies)} loaded)", "INFO")
            else:
                self.log("Running without proxy", "INFO")

            total_accounts = len(private_keys)
            self.log(f"Loaded {total_accounts} accounts successfully", "INFO")

            estimated_duration = total_accounts * tx_count * 10
            est_hours = estimated_duration // 3600
            est_minutes = (estimated_duration % 3600) // 60
            self.log(f"Estimated Cycle Duration: ~{est_hours:02d}:{est_minutes:02d} hours", "INFO")

            address_cycle = itertools.cycle(target_addresses) if target_addresses else None
            proxy_cycle = itertools.cycle(proxies) if proxies else None

            success_count = 0
            total_tx_success = 0
            total_sent_all = 0.0

            for i, pk in enumerate(private_keys):
                self.log(f"Account #{i+1}/{total_accounts}", "INFO")

                formatted_pk = pk if pk.startswith('0x') else f"0x{pk}"
                current_proxy = next(proxy_cycle) if proxy_cycle else None

                if current_proxy:
                    self.log(f"Proxy: {current_proxy}", "INFO")
                    request_kwargs = {"proxies": {"http": current_proxy, "https": current_proxy}}
                    w3 = Web3(Web3.HTTPProvider(self.rpc_url, request_kwargs=request_kwargs))
                else:
                    self.log("Proxy: No Proxy", "INFO")
                    w3 = Web3(Web3.HTTPProvider(self.rpc_url))

                try:
                    account = w3.eth.account.from_key(formatted_pk)
                    sender_address = account.address
                    self.log(f"Address: {sender_address}", "INFO")

                    if not w3.is_connected():
                        self.log("RPC Connection Failed!", "ERROR")
                        if i < total_accounts - 1:
                            print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                            time.sleep(2)
                        continue

                    balance_wei = w3.eth.get_balance(sender_address)
                    balance_eth = float(w3.from_wei(balance_wei, 'ether'))
                    self.log(f"Current Balance: {balance_eth:.6f} {self.symbol}", "INFO")

                    total_needed = amount_to_send * tx_count
                    if balance_eth < total_needed:
                        self.log(f"Insufficient balance! Need: {total_needed:.6f} {self.symbol} | Have: {balance_eth:.6f} {self.symbol}", "ERROR")
                        if i < total_accounts - 1:
                            print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                            time.sleep(2)
                        continue

                    base_nonce = w3.eth.get_transaction_count(sender_address)
                    gas_price = w3.eth.gas_price
                    gas_price_gwei = float(w3.from_wei(gas_price, 'gwei'))
                    self.log(f"Gas Price: {gas_price_gwei:.4f} Gwei", "INFO")

                    account_success_tx = 0
                    account_total_sent = 0.0

                    for tx_idx in range(tx_count):
                        print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
                        self.log(f"TX {tx_idx+1}/{tx_count}", "INFO")

                        if target_choice == '2':
                            raw_recipient = self.get_random_address()
                        else:
                            raw_recipient = next(address_cycle)

                        recipient_checksum = w3.to_checksum_address(raw_recipient)
                        self.log(f"To: {recipient_checksum}", "INFO")
                        self.log(f"Amount: {amount_to_send} {self.symbol}", "INFO")

                        tx = {
                            'nonce': base_nonce + tx_idx,
                            'to': recipient_checksum,
                            'value': w3.to_wei(amount_to_send, 'ether'),
                            'gas': 21000,
                            'gasPrice': gas_price,
                            'chainId': self.chain_id
                        }

                        signed_tx = w3.eth.account.sign_transaction(tx, formatted_pk)
                        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                        tx_hash_hex = w3.to_hex(tx_hash)

                        balance_eth -= amount_to_send
                        account_total_sent += amount_to_send

                        time_str = self.get_wib_time()
                        print(f"[{time_str}] {Fore.GREEN}[SUCCESS] TX Hash: {tx_hash_hex}{Style.RESET_ALL}")
                        print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Explorer: {self.explorer_url}/{tx_hash_hex}{Style.RESET_ALL}")
                        print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Est. Balance: ~{balance_eth:.6f} {self.symbol}{Style.RESET_ALL}")

                        account_success_tx += 1
                        total_tx_success += 1

                        if tx_idx < tx_count - 1:
                            self.random_delay(3, 10)

                    print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
                    total_sent_all += account_total_sent
                    self.log(f"Account Summary: {account_success_tx}/{tx_count} TX Success | Total Sent: {account_total_sent:.6f} {self.symbol}", "INFO")

                    if account_success_tx == tx_count:
                        success_count += 1

                except Exception as e:
                    self.log(f"Exception Occurred: {str(e)}", "ERROR")

                if i < total_accounts - 1:
                    print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                    time.sleep(2)

            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            self.log(f"Cycle #{cycle} Complete | Wallet Success: {success_count}/{total_accounts}", "CYCLE")
            self.log(f"Total TX: {total_tx_success} | Total Sent: {total_sent_all:.6f} {self.symbol}", "CYCLE")
            print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")

            cycle += 1
            self.countdown(86400)

if __name__ == "__main__":
    bot = XeneaBot()
    bot.run()
