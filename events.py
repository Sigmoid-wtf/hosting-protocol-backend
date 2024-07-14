#! /usr/bin/env python3

from web3 import Web3
from websockets import connect

import aiohttp
import asyncio
import requests

from tx import update_status
from utils import Status

CONTRACT_ADDRESS = "0xD2C1b3023760b9F3B439694255CA09205AA7E081"
CONTRACT_ABI = '[{"inputs":[{"internalType":"address","name":"relayer_","type":"address"},{"internalType":"address","name":"managerContract_","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"target","type":"address"}],"name":"AddressEmptyCode","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"AddressInsufficientBalance","type":"error"},{"inputs":[],"name":"FailedInnerCall","type":"error"},{"inputs":[],"name":"Forbidden","type":"error"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"SafeERC20FailedOperation","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint32","name":"nodeId","type":"uint32"},{"indexed":false,"internalType":"contract IERC20","name":"targetToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"string","name":"nodeType","type":"string"}],"name":"NodeCreated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint32","name":"nodeId","type":"uint32"},{"indexed":false,"internalType":"enum HostingProtocol.NodeStatus","name":"status","type":"uint8"}],"name":"StatusUpdated","type":"event"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"counter","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"managerContract","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"nodes","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"string","name":"nodeType","type":"string"},{"internalType":"enum HostingProtocol.NodeStatus","name":"status","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"relayer","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"targetToken","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"string","name":"nodeType","type":"string"}],"name":"runNode","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"managerContract_","type":"address"}],"name":"setManagerContract","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"relayer_","type":"address"}],"name":"setRelayer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"nodeId","type":"uint32"}],"name":"stopNode","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"nodeId","type":"uint32"},{"internalType":"enum HostingProtocol.NodeStatus","name":"status","type":"uint8"}],"name":"updateStatus","outputs":[],"stateMutability":"nonpayable","type":"function"}]'


async def handle_event(session: aiohttp.ClientSession, event):
    print(Web3.to_json(event))
    node_id, status = event["args"]["nodeId"], Status(event["args"]["status"])
    if status == Status.QUEUED:
        await session.post("http://localhost:8000/create", params={"node_id": str(node_id)})
        print(f"Setting status of {node_id} to {Status.RUNNING.value}")
        update_status(node_id, Status.RUNNING.value)
    elif status == Status.STOPPING:
        await session.post("http://localhost:8000/stop", params={"node_id": str(node_id)})
        print(f"Setting status of {node_id} to {Status.DOWN.value}")
        update_status(node_id, Status.DOWN.value)


async def log_loop(event_filter, poll_interval):
    session = aiohttp.ClientSession('http://localhost:8000')
    while True:
        for event in event_filter.get_new_entries():
            await handle_event(session, event)
        await asyncio.sleep(poll_interval)


def main():
    w3 = Web3(Web3.WebsocketProvider("wss://eth-sepolia.g.alchemy.com/v2/Qlr3apDsKG7I7tlI8YGwXtxDVeyT0Kzv"))
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

    event_filter = contract.events.StatusUpdated.create_filter(fromBlock="latest")
    print(event_filter)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(log_loop(event_filter, 2)))
    finally:
        loop.close()


if __name__ == "__main__":
    main()
