from web3 import Web3
from brownie import network
import os

if network.show_active() == 'anvil':
    web3 = Web3(Web3.HTTPProvider(f"http://127.0.0.1:8545"))
else:
    web3 = Web3(Web3.HTTPProvider(f"http://localhost:8545"))
