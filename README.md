# XENEA UBUSUNA BOT

Automated transaction bot for the **Xenea Ubusuna** testnet network. Supports multi-account, proxy, and random/custom destination address features.

---

## Features

- ✅ Multi-account support via `accounts.txt`
- ✅ Custom or random destination address
- ✅ Proxy support (HTTP)
- ✅ Configurable TX count per account
- ✅ Auto countdown for next cycle (24 hours)
- ✅ Colored terminal output with real-time logging
- ✅ WIB (Asia/Jakarta) timezone display

---

## Requirements

- Python 3.8+
- Install dependencies:

```bash
pip install web3 eth-account colorama pytz
```

---

## Setup

1. **Clone the repository:**
```bash
git clone https://github.com/febriyan9346/XENEA-UBUSUNA-BOT.git
cd XENEA-UBUSUNA-BOT
```

2. **Create `accounts.txt`** — one private key per line:
```
0xYOUR_PRIVATE_KEY_1
0xYOUR_PRIVATE_KEY_2
```

3. *(Optional)* **Create `address.txt`** — one address per line (if using custom destination):
```
0xRecipientAddress1
0xRecipientAddress2
```

4. *(Optional)* **Create `proxy.txt`** — one proxy per line:
```
http://user:pass@ip:port
```

---

## Usage

```bash
python bot.py
```

Follow the interactive prompts to:
- Choose proxy mode
- Choose destination (from `address.txt` or random)
- Set transfer amount
- Set TX count per account

---

## Network Info

| Parameter | Value |
|-----------|-------|
| Network   | Xenea Ubusuna Testnet |
| RPC URL   | https://rpc-ubusuna.xeneascan.com |
| Chain ID  | 1096 |
| Symbol    | TXENE |
| Explorer  | https://xeneascan.com |

---

## Disclaimer

> This bot is intended for **testnet use only**. Use at your own risk. The author is not responsible for any loss of funds.

---

## Support Us with Cryptocurrency

You can make a contribution using any of the following blockchain networks:

| Network | Wallet Address |
|---------|---------------|
| EVM | `0x216e9b3a5428543c31e659eb8fea3b4bf770bdfd` |
| TON | `UQCEzXLDalfKKySAHuCtBZBARCYnMc0QsTYwN4qda3fE6tto` |
| SOL | `9XgbPg8fndBquuYXkGpNYKHHhymdmVhmF6nMkPxhXTki` |
| SUI | `0x8c3632ddd46c984571bf28f784f7c7aeca3b8371f146c4024f01add025f993bf` |
