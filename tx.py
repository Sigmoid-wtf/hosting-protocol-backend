#! /usr/bin/env python3

from web3 import Web3
from websockets import connect

CONTRACT_ADDRESS = "0xD2C1b3023760b9F3B439694255CA09205AA7E081"
CONTRACT_ABI = '[{"inputs":[{"internalType":"address","name":"relayer_","type":"address"},{"internalType":"address","name":"managerContract_","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"target","type":"address"}],"name":"AddressEmptyCode","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"AddressInsufficientBalance","type":"error"},{"inputs":[],"name":"FailedInnerCall","type":"error"},{"inputs":[],"name":"Forbidden","type":"error"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"SafeERC20FailedOperation","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint32","name":"nodeId","type":"uint32"},{"indexed":false,"internalType":"contract IERC20","name":"targetToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"string","name":"nodeType","type":"string"}],"name":"NodeCreated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint32","name":"nodeId","type":"uint32"},{"indexed":false,"internalType":"enum HostingProtocol.NodeStatus","name":"status","type":"uint8"}],"name":"StatusUpdated","type":"event"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"counter","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"managerContract","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"nodes","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"string","name":"nodeType","type":"string"},{"internalType":"enum HostingProtocol.NodeStatus","name":"status","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"relayer","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"targetToken","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"string","name":"nodeType","type":"string"}],"name":"runNode","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"managerContract_","type":"address"}],"name":"setManagerContract","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"relayer_","type":"address"}],"name":"setRelayer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"nodeId","type":"uint32"}],"name":"stopNode","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"nodeId","type":"uint32"},{"internalType":"enum HostingProtocol.NodeStatus","name":"status","type":"uint8"}],"name":"updateStatus","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

TOKEN_ADDRESS = "0x5d5DE7668C6979Ce17BB6760490D160137066628"
TOKEN_ABI = '[{"inputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"symbol","type":"string"},{"internalType":"uint8","name":"decimals","type":"uint8"},{"internalType":"address","name":"owner","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"target","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

PRIVATE_KEY = "XXX"


W3 = Web3(Web3.WebsocketProvider("wss://ethereum-sepolia-rpc.publicnode.com"))
CONTRACT = W3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
COIN = W3.eth.contract(address=TOKEN_ADDRESS, abi=TOKEN_ABI)
ACC = W3.eth.account.from_key(PRIVATE_KEY)


def send():
    amount = W3.to_wei(10, "ether")
    tx = COIN.functions.transfer("0x58a1ea996831599D2234a801c3B192Dd5e800d88", amount).build_transaction({
        "from": ACC.address,
        "nonce": W3.eth.get_transaction_count(ACC.address)
    })

    signed_tx = ACC.sign_transaction(tx)
    tx_hash = W3.eth.send_raw_transaction(signed_tx.rawTransaction)
    W3.eth.wait_for_transaction_receipt(tx_hash)


def approve():
    amount = W3.to_wei(1000, "ether")
    tx = COIN.functions.approve(CONTRACT_ADDRESS, amount).build_transaction({
        "from": ACC.address,
        "nonce": W3.eth.get_transaction_count(ACC.address)
    })
    signed_tx = ACC.sign_transaction(tx)
    tx_hash = W3.eth.send_raw_transaction(signed_tx.rawTransaction)
    W3.eth.wait_for_transaction_receipt(tx_hash)


def update_status(node_id, status):
    tx = CONTRACT.functions.updateStatus(node_id, status).build_transaction({
        "from": ACC.address,
        "nonce": W3.eth.get_transaction_count(ACC.address)
    })
    signed_tx = ACC.sign_transaction(tx)
    tx_hash = W3.eth.send_raw_transaction(signed_tx.rawTransaction)
    W3.eth.wait_for_transaction_receipt(tx_hash)


def main():
    amount = W3.to_wei(10, "ether")
    print(TOKEN_ADDRESS.lower())
    tx = CONTRACT.functions.runNode(TOKEN_ADDRESS, amount, "HUI").build_transaction({
        "from": ACC.address,
        "nonce": W3.eth.get_transaction_count(ACC.address)
    })
    signed_tx = ACC.sign_transaction(tx)
    tx_hash = W3.eth.send_raw_transaction(signed_tx.rawTransaction)
    W3.eth.wait_for_transaction_receipt(tx_hash)


if __name__ == "__main__":
    main()
