

import secrets
import string
import time
import json
from eth_utils import keccak, to_bytes, to_hex

from web3 import Web3, HTTPProvider, Account, WebsocketProvider, IPCProvider
from web3.middleware import geth_poa_middleware


HTTPProvider = HTTPProvider('https://bsc-dataseed1.bnbchain.org')
# WebsocketProvider = WebsocketProvider('wss://rpc-bsc.48.club/ws')
w3 = Web3(HTTPProvider)

w3.middleware_onion.inject(geth_poa_middleware, layer=0)  # Inject POA middleware

Perpetual_Motion_Machine_ABI_FILE = open(file='abis/Perpetual_Motion_Machine.json')
Perpetual_Motion_Machine_ABI = json.loads(Perpetual_Motion_Machine_ABI_FILE.read())['abi']
Perpetual_Motion_Machine_CA = w3.to_checksum_address('0x6A5da7CD28AA08C1aC601343d85a11648Eb8bA96')
Perpetual_Motion_Machine_contract = w3.eth.contract(address = Perpetual_Motion_Machine_CA, abi = Perpetual_Motion_Machine_ABI)
# print(Perpetual_Motion_Machine_ABI)


def getLastDifficulty():

    last_difficulty = Perpetual_Motion_Machine_contract.functions.getLastdifficulty().call()
    return last_difficulty

def random_hex(_seed):
  # 
    random_hex = secrets.token_hex(15)  
    s = _seed + random_hex
    return s


def keccak256_abi_encode_packed(_msg_sender, _seed):
    msg_sender_bytes = to_bytes(hexstr=_msg_sender)
    seed_bytes = to_bytes(text=_seed)

    packed_data = msg_sender_bytes + seed_bytes
    hash_result = keccak(packed_data)
    return to_hex(hash_result)

def send_tx(_the_seed):
    tx = Perpetual_Motion_Machine_contract.functions.mint(
    _the_seed

    ).build_transaction({
        'type': '0x2',  
        'chainId': w3.eth.chain_id,
        'nonce': w3.eth.get_transaction_count(msg_sender, 'latest'),
        'maxPriorityFeePerGas': w3.to_wei('1', 'gwei'),
        'maxFeePerGas': w3.to_wei('1', 'gwei'),
        'gas': 300000,
        'value': 0,
    })
    signed_txn = w3.eth.account.sign_transaction(tx, private_key=key)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    print(f"Transaction hash: https://bscscan.com/tx/{tx_hash.hex()}")        

        
msg_sender = w3.to_checksum_address("address")
key = 'priv key'
# seed prefix.
seed = "The combination of POW mining and POS chain, standard ERC20 tokens, convenient ecological construction complete decentralized exchange support, PMM will definitely change the method of changing community tokens. Add the PMM mining, now. "


mint = 0
last_difficulty = getLastDifficulty()

while mint < 100:

    the_seed = random_hex(seed)

    the_hash = keccak256_abi_encode_packed(msg_sender, the_seed)
    if to_hex(last_difficulty) > the_hash:
        print(f"Got the result,Seed: {the_seed}, Hash: {the_hash}, Last_Difficulty: {to_hex(last_difficulty)}, Mint_Times: {mint}")
        send_tx(the_seed)                
        mint += 1
        time.sleep(5)
        print(to_hex(last_difficulty))
        last_difficulty = getLastDifficulty()


