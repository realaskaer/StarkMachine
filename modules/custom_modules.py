import random

from general_settings import GLOBAL_NETWORK
from modules import Logger, RequestClient
from modules.interfaces import SoftwareExceptionWithoutRetry
from utils.tools import helper, gas_checker, sleep
from config import (
    ETH_PRICE, TOKENS_PER_CHAIN, CHAIN_NAME, OKX_NETWORKS_NAME, BINGX_NETWORKS_NAME, BINANCE_NETWORKS_NAME, CEX_WRAPPED_ID,
    COINGECKO_TOKEN_API_NAMES
)
from settings import (
    CEX_BALANCE_WANTED, OKX_WITHDRAW_DATA, BINANCE_DEPOSIT_DATA,
    BINGX_WITHDRAW_DATA, BINANCE_WITHDRAW_DATA,
    CEX_DEPOSIT_LIMITER, RHINO_CHAIN_ID_FROM, LAYERSWAP_CHAIN_ID_FROM, ORBITER_CHAIN_ID_FROM, BRIDGE_AMOUNT_LIMITER,
    ORBITER_TOKEN_NAME, LAYERSWAP_TOKEN_NAME, OKX_DEPOSIT_DATA, BINGX_DEPOSIT_DATA
)


class Custom(Logger, RequestClient):
    def __init__(self, client):
        self.client = client
        Logger.__init__(self)
        RequestClient.__init__(self, client)

    async def collect_eth_util(self):
        if GLOBAL_NETWORK == 9:
            await self.client.initialize_account()

        from functions import swap_avnu, swap_rango

        self.logger_msg(*self.client.acc_info, msg=f"Started collecting tokens in ETH")

        func = {
            'Starknet': [swap_rango, swap_avnu]
        }[self.client.network.name]

        wallet_balance = {k: await self.client.get_token_balance(k, False)
                          for k, v in TOKENS_PER_CHAIN[self.client.network.name].items()}
        valid_wallet_balance = {k: v[1] for k, v in wallet_balance.items() if v[0] != 0}
        eth_price = ETH_PRICE

        for token in ['ETH', 'WETH']:
            if token in valid_wallet_balance:
                valid_wallet_balance[token] *= eth_price

        if valid_wallet_balance['ETH'] < 0.5:
            self.logger_msg(*self.client.acc_info, msg=f'Account has not enough ETH for swap', type_msg='warning')
            return True

        if len(valid_wallet_balance.values()) > 1:
            try:
                for token_name, token_balance in valid_wallet_balance.items():
                    if token_name != 'ETH':
                        amount_in_wei = wallet_balance[token_name][0]
                        amount = float(f"{(amount_in_wei / 10 ** await self.client.get_decimals(token_name)):.6f}")
                        amount_in_usd = valid_wallet_balance[token_name]
                        if amount_in_usd > 1:
                            from_token_name, to_token_name = token_name, 'ETH'
                            data = from_token_name, to_token_name, amount, amount_in_wei
                            counter = 0
                            while True:
                                result = False
                                module_func = random.choice(func)
                                try:
                                    self.logger_msg(*self.client.acc_info, msg=f'Launching swap module', type_msg='warning')
                                    result = await module_func(self.client.account_name, self.client.private_key,
                                                               self.client.network, self.client.proxy_init, swapdata=data)
                                    if not result:
                                        counter += 1
                                except:
                                    counter += 1
                                    pass
                                if result or counter == 3:
                                    break
                        else:
                            self.logger_msg(*self.client.acc_info, msg=f"{token_name} balance < 1$")
            except Exception as error:
                self.logger_msg(*self.client.acc_info, msg=f"Error in collector route. Error: {error}")
        else:
            self.logger_msg(*self.client.acc_info, msg=f"Account balance already in ETH!", type_msg='warning')

    @helper
    async def collect_eth(self):
        await self.collect_eth_util()

        return True

    @helper
    async def balance_average(self):
        if GLOBAL_NETWORK == 9:
            await self.client.initialize_account()

        from functions import okx_withdraw_util

        self.logger_msg(*self.client.acc_info, msg=f"Stark check all balance to make average")

        amount = CEX_BALANCE_WANTED
        wanted_amount_in_usd = float(f'{amount * ETH_PRICE:.2f}')

        wallet_balance = {k: await self.client.get_token_balance(k, False)
                          for k, v in TOKENS_PER_CHAIN[self.client.network.name].items()}
        valid_wallet_balance = {k: v[1] for k, v in wallet_balance.items() if v[0] != 0}
        eth_price = ETH_PRICE

        if 'ETH' in valid_wallet_balance:
            valid_wallet_balance['ETH'] = valid_wallet_balance['ETH'] * eth_price

        valid_wallet_balance = {k: round(v, 7) for k, v in valid_wallet_balance.items()}

        sum_balance_in_usd = sum(valid_wallet_balance.values())

        if wanted_amount_in_usd > sum_balance_in_usd:
            need_to_withdraw = float(f"{(wanted_amount_in_usd - sum_balance_in_usd) / eth_price:.6f}")

            self.logger_msg(*self.client.acc_info, msg=f"Not enough balance on account, start OKX withdraw module")

            return await okx_withdraw_util(self.client, want_balance=need_to_withdraw)
        raise SoftwareExceptionWithoutRetry('Account has enough tokens on balance!')

    async def balance_searcher(self, chains, tokens, bridge_check:bool = False):

        clients = [await self.client.new_client(chain)
                   for chain in chains]

        balances = [await client.get_token_balance(token_name=token, bridge_check=bridge_check)
                    for client, token in zip(clients, tokens)]

        balances_in_usd = []
        for balance_in_wei, balance, token_name in balances:
            token_price = 1
            if 'USD' not in token_name:
                token_price = await self.client.get_token_price(COINGECKO_TOKEN_API_NAMES[token_name])
            balance_in_usd = balance * token_price
            balances_in_usd.append([balance_in_usd, token_price])

        index = balances_in_usd.index(max(balances_in_usd, key=lambda x: x[0]))

        for index_client, client in enumerate(clients):
            if index_client != index:
                await client.session.close()

        self.logger_msg(
            *self.client.acc_info,
            msg=f"Detected {round(balances[index][1], 5)} {tokens[index]} in {clients[index].network.name}",
            type_msg='success')

        return clients[index], index, balances[index][1], balances_in_usd[index]

    @helper
    async def smart_cex_withdraw(self, dapp_id:int):
        if GLOBAL_NETWORK == 9:
            await self.client.initialize_account()

        from functions import okx_withdraw_util, bingx_withdraw_util, binance_withdraw_util

        func, multi_withdraw_data = {
            1: (okx_withdraw_util, OKX_WITHDRAW_DATA),
            2: (bingx_withdraw_util, BINGX_WITHDRAW_DATA),
            3: (binance_withdraw_util, BINANCE_WITHDRAW_DATA)
        }[dapp_id]

        random.shuffle(multi_withdraw_data)

        for data in multi_withdraw_data:
            current_data = data
            if isinstance(data[0], list):
                current_data = random.choice(data)
                if not current_data:
                    continue

            network, amount = current_data
            if isinstance(amount[0], str):
                raise SoftwareExceptionWithoutRetry('CEX withdrawal does not support % of the amount')

            try:
                await func(self.client, withdraw_data=(network, amount))

            except Exception as error:
                self.logger_msg(
                    *self.client.acc_info, msg=f"Withdraw from CEX failed. Error: {error}", type_msg='error')

            await sleep(self)

        return True

    @helper
    async def smart_cex_withdraw(self, dapp_id: int):
        if GLOBAL_NETWORK == 9:
            await self.client.initialize_account()

        from functions import okx_withdraw_util, bingx_withdraw_util, binance_withdraw_util

        func, multi_withdraw_data = {
            1: (okx_withdraw_util, OKX_WITHDRAW_DATA),
            2: (bingx_withdraw_util, BINGX_WITHDRAW_DATA),
            3: (binance_withdraw_util, BINANCE_WITHDRAW_DATA)
        }[dapp_id]

        random.shuffle(multi_withdraw_data)

        for data in multi_withdraw_data:
            current_data = data
            if isinstance(data[0], list):
                current_data = random.choice(data)
                if not current_data:
                    continue

            network, amount = current_data
            if isinstance(amount[0], str):
                raise SoftwareExceptionWithoutRetry('CEX withdrawal does not support % of the amount')

            try:
                await func(self.client, withdraw_data=(network, amount))

            except Exception as error:
                self.logger_msg(
                    *self.client.acc_info, msg=f"Withdraw from CEX failed. Error: {error}", type_msg='error')

            await sleep(self)

        return True

    @helper
    @gas_checker
    async def smart_cex_deposit(self, dapp_id:int):
        if GLOBAL_NETWORK == 9:
            await self.client.initialize_account()

        client = None
        try:
            from functions import cex_deposit_util

            class_id, multi_deposit_data, cex_config = {
                1: (1, OKX_DEPOSIT_DATA, OKX_NETWORKS_NAME),
                2: (2, BINGX_DEPOSIT_DATA, BINGX_NETWORKS_NAME),
                3: (3, BINANCE_DEPOSIT_DATA, BINANCE_NETWORKS_NAME),
            }[dapp_id]

            for data in multi_deposit_data:
                current_data = data
                if isinstance(data[0], list):
                    current_data = random.choice(data)
                    if not current_data:
                        continue

                networks, amount = current_data
                if isinstance(networks, tuple):
                    dapp_tokens = [f"{cex_config[network].split('-')[0]}{'.e' if network in [30, 31] else ''}"
                                   for network in networks]
                    dapp_chains = [CEX_WRAPPED_ID[chain] for chain in networks]
                else:
                    dapp_tokens = [cex_config[networks].split('-')[0]]
                    dapp_chains = [CEX_WRAPPED_ID[networks]]

                client, chain_index, balance, balance_data = await self.balance_searcher(
                    chains=dapp_chains, tokens=dapp_tokens,
                )

                balance_in_usd, token_price = balance_data
                dep_token = dapp_tokens[chain_index]
                dep_network = networks if isinstance(networks, int) else networks[chain_index]
                limit_amount, wanted_to_hold_amount = CEX_DEPOSIT_LIMITER
                min_wanted_amount, max_wanted_amount = min(wanted_to_hold_amount), max(wanted_to_hold_amount)

                if balance_in_usd > limit_amount:

                    dep_amount = await client.get_smart_amount(amount)
                    dep_amount_in_usd = dep_amount * token_price

                    if balance_in_usd > dep_amount_in_usd:

                        if min_wanted_amount <= (balance_in_usd - dep_amount_in_usd) <= max_wanted_amount:

                            deposit_data = dep_network, (dep_amount, dep_amount)

                            return await cex_deposit_util(client, dapp_id=class_id, deposit_data=deposit_data)

                        hold_amount_in_usd = balance_in_usd - dep_amount_in_usd
                        info = f"{min_wanted_amount:.2f}$ <= {hold_amount_in_usd:.2f}$ <= {max_wanted_amount:.2f}$"
                        raise SoftwareExceptionWithoutRetry(f'Account balance will be not in wanted hold amount: {info}')

                    info = f"{balance_in_usd:.2f}$ < {dep_amount_in_usd:.2f}$"
                    raise SoftwareExceptionWithoutRetry(f'Account {dep_token} balance < wanted deposit amount: {info}')

                info = f"{balance_in_usd:.2f}$ < {limit_amount:.2f}$"
                raise SoftwareExceptionWithoutRetry(f'Account {dep_token} balance < wanted limit amount: {info}')
        finally:
            await client.session.close()

    @helper
    @gas_checker
    async def smart_bridge(self, dapp_id:int = None, private_keys:dict=None):
        if GLOBAL_NETWORK == 9:
            await self.client.initialize_account()

        client = None
        try:
            from functions import bridge_utils

            bridge_app_id, dapp_chains, dapp_token = {
                1: (1, LAYERSWAP_CHAIN_ID_FROM, LAYERSWAP_TOKEN_NAME),
                2: (2, ORBITER_CHAIN_ID_FROM, ORBITER_TOKEN_NAME),
                3: (3, RHINO_CHAIN_ID_FROM, 'ETH'),
            }[dapp_id]

            dapp_tokens = [dapp_token for _ in dapp_chains]

            client, chain_index, balance, balance_data = await self.balance_searcher(
                chains=dapp_chains, tokens=dapp_tokens, bridge_check=True
            )

            chain_from_id, token_name = dapp_chains[chain_index], dapp_token

            source_chain_name, destination_chain, amount, dst_chain_id = await client.get_bridge_data(
                chain_from_id=chain_from_id, dapp_id=bridge_app_id
            )

            from_token_addr = None
            to_token_addr = None
            from_chain_name = client.network.name
            to_chain_name = CHAIN_NAME[dst_chain_id]
            if token_name == 'USDC':
                from_token_addr = TOKENS_PER_CHAIN[from_chain_name].get('USDC.e')
                to_token_addr = TOKENS_PER_CHAIN[to_chain_name].get('USDC.e')
            from_token_addr = from_token_addr if from_token_addr else TOKENS_PER_CHAIN[from_chain_name][token_name]
            to_token_addr = to_token_addr if to_token_addr else TOKENS_PER_CHAIN[to_chain_name][token_name]

            balance_in_usd, token_price = balance_data
            limit_amount, wanted_to_hold_amount = BRIDGE_AMOUNT_LIMITER
            min_wanted_amount, max_wanted_amount = min(wanted_to_hold_amount), max(wanted_to_hold_amount)
            bridge_data = (source_chain_name, destination_chain, amount,
                           dst_chain_id, token_name, from_token_addr, to_token_addr)

            if balance_in_usd > limit_amount:

                bridge_amount = await bridge_utils(client, bridge_app_id, chain_from_id, bridge_data, private_keys=private_keys, need_fee=True)
                bridge_amount_in_usd = bridge_amount * token_price

                if balance_in_usd > bridge_amount_in_usd:

                    if min_wanted_amount <= (balance_in_usd - bridge_amount_in_usd) <= max_wanted_amount:

                        return await bridge_utils(client, bridge_app_id, chain_from_id, bridge_data, private_keys=private_keys)

                    hold_amount_in_usd = balance_in_usd - bridge_amount_in_usd
                    info = f"{min_wanted_amount:.2f}$ <= {hold_amount_in_usd:.2f}$ <= {max_wanted_amount:.2f}$"
                    raise SoftwareExceptionWithoutRetry(f'Account balance will be not in wanted hold amount: {info}')

                info = f"{balance_in_usd:.2f}$ < {bridge_amount_in_usd:.2f}$"
                raise SoftwareExceptionWithoutRetry(f'Account {token_name} balance < wanted bridge amount: {info}')

            info = f"{balance_in_usd:.2f}$ < {limit_amount:.2f}$"
            raise SoftwareExceptionWithoutRetry(f'Account {token_name} balance < wanted limit amount: {info}')
        finally:
            await client.session.close()
