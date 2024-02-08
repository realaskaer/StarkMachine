import random

from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.full_node_client import FullNodeClient


from eth_account import Account
from modules import Blockchain, Logger, Bridge
from modules.interfaces import SoftwareException
from utils.networks import StarknetRPC
from utils.tools import gas_checker, helper
from general_settings import TRANSFER_AMOUNT
from settings import NATIVE_BRIDGE_AMOUNT

from config import (
    WETH_ABI,
    TOKENS_PER_CHAIN,
    NATIVE_CONTRACTS_PER_CHAIN,
    NATIVE_ABI,
)


class SimpleEVM(Logger):
    def __init__(self, client):
        self.client = client
        Logger.__init__(self)

        self.network = self.client.network.name
        self.token_contract = self.client.get_contract(
            TOKENS_PER_CHAIN[self.client.network.name]['WETH'], WETH_ABI)
        if self.network in ['zkSync']:
            self.deposit_contract = self.client.get_contract(
                NATIVE_CONTRACTS_PER_CHAIN[self.network]['deposit'],
                NATIVE_ABI[self.network]['deposit'])
            self.withdraw_contract = self.client.get_contract(
                NATIVE_CONTRACTS_PER_CHAIN[self.network]['withdraw'],
                NATIVE_ABI[self.network]['withdraw'])
        else:
            pass

    @helper
    @gas_checker
    async def deploy_contract(self):

        try:
            with open('data/services/contact_data.json') as file:
                from json import load
                contract_data = load(file)
        except:
            raise SoftwareException("Bad data in contract_json.json")

        self.logger_msg(*self.client.acc_info, msg=f"Deploy contract on {self.client.network.name}")

        tx_data = await self.client.prepare_transaction()

        contract = self.client.w3.eth.contract(abi=contract_data['abi'], bytecode=contract_data['bytecode'])

        transaction = await contract.constructor().build_transaction(tx_data)

        return await self.client.send_transaction(transaction)

    @helper
    @gas_checker
    async def transfer_eth_to_myself(self):

        amount, amount_in_wei = await self.client.get_smart_amount(TRANSFER_AMOUNT)

        self.logger_msg(*self.client.acc_info, msg=f"Transfer {amount} ETH to your own address: {self.client.address}")

        tx_params = await self.client.prepare_transaction(value=amount_in_wei) | {
            "to": self.client.address,
            "data": "0x"
        }

        return await self.client.send_transaction(tx_params)

    @helper
    @gas_checker
    async def transfer_eth(self):

        amount, amount_in_wei = await self.client.get_smart_amount(TRANSFER_AMOUNT)

        random_address = Account.create().address

        self.logger_msg(*self.client.acc_info, msg=f'Transfer ETH to random zkSync address: {amount} ETH')

        if await self.client.w3.eth.get_balance(self.client.address) > amount_in_wei:

            tx_params = (await self.client.prepare_transaction()) | {
                'to': random_address,
                'value': amount_in_wei,
                'data': "0x"
            }

            return await self.client.send_transaction(tx_params)

        else:
            raise SoftwareException('Insufficient balance!')


class StarknetEVM(Blockchain, Logger, Bridge):
    def __init__(self, client):
        self.client = client
        Logger.__init__(self)
        Bridge.__init__(self, client)
        Blockchain.__init__(self, client)

        self.evm_contract = self.client.get_contract(NATIVE_CONTRACTS_PER_CHAIN['Starknet']['evm_contract'],
                                                     NATIVE_ABI['Starknet']['evm_contract'])

    async def bridge(self, *args, **kwargs):
        pass

    async def get_starknet_deposit_fee(self, amount_in_wei: int):
        stark_w3 = FullNodeClient(random.choice(StarknetRPC.rpc))
        return (await stark_w3.estimate_message_fee(
            from_address=NATIVE_CONTRACTS_PER_CHAIN['Starknet']['evm_contract'],
            to_address=NATIVE_CONTRACTS_PER_CHAIN['Starknet']['stark_contract'],
            entry_point_selector=get_selector_from_name("handle_deposit"),
            payload=[
                int(self.client.address, 16),
                amount_in_wei,
                0
            ]
        )).overall_fee

    @helper
    @gas_checker
    async def deposit(self, private_keys:dict = None):

        receiver = await self.get_address_for_bridge(private_keys['stark_key'], stark_key_type=True)

        amount = await self.client.get_smart_amount(NATIVE_BRIDGE_AMOUNT)
        amount_in_wei = int(amount * 10 ** 18)

        self.logger_msg(self.client.account_name, None,
                        msg=f'Bridge on StarkGate to {receiver}: {amount} ETH ERC20 -> Starknet')

        deposit_fee = await self.get_starknet_deposit_fee(amount_in_wei)

        tx_params = await self.client.prepare_transaction(value=amount_in_wei + deposit_fee)

        transaction = await self.evm_contract.functions.deposit(
            amount_in_wei,
            int(receiver, 16)
        ).build_transaction(tx_params)

        return await self.client.send_transaction(transaction)

    async def withdraw(self):
        pass  # реализовано в Starknet

