import random

from modules import Landing, Logger, StarknetClient
from utils.tools import gas_checker, helper
from config import ZKLEND_CONTRACTS, TOKENS_PER_CHAIN


class ZkLend(Landing, Logger):
    def __init__(self, client: StarknetClient):
        self.client = client
        Logger.__init__(self)

    @helper
    @gas_checker
    async def deposit(self):
        await self.client.initialize_account()

        token_name, token_address, amount, amount_in_wei = await self.client.get_landing_data('zkLend', True)

        self.logger_msg(*self.client.acc_info, msg=f'Deposit to zkLend: {amount} {token_name}')

        landing_contract = await self.client.get_contract(ZKLEND_CONTRACTS['landing'])

        approve_call = self.client.get_approve_call(token_address, ZKLEND_CONTRACTS['landing'],
                                                    amount_in_wei)

        deposit_call = landing_contract.functions["deposit"].prepare_call(
            [
                token_address,
                amount_in_wei
            ]
        )

        return await self.client.send_transaction(approve_call, deposit_call)

    @helper
    @gas_checker
    async def withdraw(self):
        await self.client.initialize_account()

        token_name, token_contract = await self.client.get_landing_data(class_name='zkLend')

        landing_balance = (await self.client.account.client.call_contract(self.client.prepare_call(
            contract_address=ZKLEND_CONTRACTS[token_name],
            selector_name='balanceOf',
            calldata=[self.client.address]
        )))[0]

        decimals = (await self.client.account.client.call_contract(self.client.prepare_call(
            contract_address=ZKLEND_CONTRACTS[token_name],
            selector_name='decimals',
            calldata=[]
        )))[0]

        self.logger_msg(
            *self.client.acc_info, msg=f'Withdraw {landing_balance / 10 ** decimals:.5f} {token_name} from zkLend'
        )

        landing_contract = await self.client.get_contract(ZKLEND_CONTRACTS['landing'])

        withdraw_call = landing_contract.functions["withdraw"].prepare_call(
            token_contract,
            landing_balance
        )

        return await self.client.send_transaction(withdraw_call)

    @helper
    @gas_checker
    async def enable_collateral(self):
        await self.client.initialize_account()

        token_name, token_address = random.choice(list(TOKENS_PER_CHAIN[self.client.network.name].items()))

        self.logger_msg(*self.client.acc_info, msg=f'Enable {token_name} collateral on zkLend')

        landing_contract = await self.client.get_contract(ZKLEND_CONTRACTS['landing'])

        enable_collateral_call = landing_contract.functions["enable_collateral"].prepare_call(
            [
                token_address
            ]
        )

        return await self.client.send_transaction(enable_collateral_call)

    @helper
    @gas_checker
    async def disable_collateral(self):
        await self.client.initialize_account()

        token_name, token_address = random.choice(list(TOKENS_PER_CHAIN[self.client.network.name].items()))

        self.logger_msg(*self.client.acc_info, msg=f'Disable {token_name} collateral on zkLend')

        landing_contract = await self.client.get_contract(ZKLEND_CONTRACTS['landing'])

        disable_collateral_call = landing_contract.functions["disable_collateral"].prepare_call(
            [
                token_address
            ]
        )

        return await self.client.send_transaction(disable_collateral_call)
