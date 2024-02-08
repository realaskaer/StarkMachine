import asyncio
import os
import json

from utils.tools import clean_progress_file
from functions import *
from web3 import AsyncWeb3
from config import ACCOUNT_NAMES
from modules import Logger
from modules.interfaces import SoftwareException
from gspread.utils import rowcol_to_a1
from gspread import Client, Spreadsheet, Worksheet, service_account
from general_settings import GOOGLE_SHEET_URL, GOOGLE_SHEET_PAGE_NAME, GLOBAL_NETWORK, SHUFFLE_ROUTE
from settings import (MODULES_COUNT, ALL_MODULES_TO_RUN,
                      TRANSFER_IN_ROUTES, TRANSFER_COUNT, EXCLUDED_MODULES,
                      DMAIL_IN_ROUTES, DMAIL_COUNT, COLLATERAL_IN_ROUTES, COLLATERAL_COUNT,
                      CLASSIC_ROUTES_MODULES_USING, WITHDRAW_LANDING, HELPERS_CONFIG,
                      CLASSIC_WITHDRAW_DEPENDENCIES)

GSHEET_CONFIG = "./data/services/service_account.json"
os.environ["GSPREAD_SILENCE_WARNINGS"] = "1"


AVAILABLE_MODULES_INFO = {
    # module_name                       : (module name, priority, tg info, can be help module, supported network)
    okx_withdraw                        : (okx_withdraw, -3, 'OKX Withdraw', 0, []),
    bingx_withdraw                      : (bingx_withdraw, -3, 'BingX Withdraw', 0, []),
    binance_withdraw                    : (binance_withdraw, -3, 'Binance Withdraw', 0, []),
    make_balance_to_average             : (make_balance_to_average, -2, 'Check and make wanted balance', 0, []),
    deploy_stark_wallet                 : (deploy_stark_wallet, 0, 'Deploy Wallet', 0, [9]),
    bridge_rhino                        : (bridge_rhino, 1, 'Rhino Bridge', 0, [2, 3, 4, 8, 9, 11, 12]),
    bridge_layerswap                    : (bridge_layerswap, 1, 'LayerSwap Bridge', 0, [2, 3, 4, 8, 9, 11, 12]),
    bridge_orbiter                      : (bridge_orbiter, 1, 'Orbiter Bridge', 0, [2, 3, 4, 8, 9, 11, 12]),
    bridge_native                       : (bridge_native, 1, 'Native Bridge', 0, [2, 3, 4, 8, 9, 11, 12]),
    upgrade_stark_wallet                : (upgrade_stark_wallet, 2, 'Upgrade Wallet', 0, [9]),
    deposit_nostra                      : (deposit_nostra, 2, 'Nostra Deposit', 0, [9]),
    deposit_zklend                      : (deposit_zklend, 2, 'zkLend Deposit', 0, [9]),
    enable_collateral_zklend            : (enable_collateral_zklend, 2, 'Enable zkLend Collateral', 1, [9]),
    swap_jediswap                       : (swap_jediswap, 2, 'JediSwap Swap', 1, [9]),
    swap_avnu                           : (swap_avnu, 2, 'AVNU Swap', 1, [9]),
    swap_10kswap                        : (swap_10kswap, 2, '10kSwap Swap', 1, [9]),
    swap_sithswap                       : (swap_sithswap, 2, 'SithSwap Swap', 1, [9]),
    swap_protoss                        : (swap_protoss, 2, 'Protoss Swap', 1, [9]),
    swap_myswap                         : (swap_myswap, 2, 'mySwap Swap', 1, [9]),
    swap_rango                          : (swap_rango, 2, 'Rango Swap', 1, [4, 11]),
    random_approve                      : (random_approve, 2, 'Random Approve', 0, []),
    disable_collateral_zklend           : (disable_collateral_zklend, 2, 'Disable zkLend Collateral', 1, [9]),
    mint_starknet_identity              : (mint_starknet_identity, 2, 'Mint Starknet ID', 0, [9]),
    mint_starkstars                     : (mint_starkstars, 2, 'StarkStars Mint', 0, [9]),
    send_message_dmail                  : (send_message_dmail, 2, 'Dmail Message', 1, [3, 4, 8, 9, 11]),
    transfer_eth                        : (transfer_eth, 2, 'Transfer ETH', 0, []),
    transfer_eth_to_myself              : (transfer_eth_to_myself, 2, 'Transfer ETH to myself', 0, []),
    withdraw_nostra                     : (withdraw_nostra, 3, 'Nostra Withdraw', 0, []),
    withdraw_zklend                     : (withdraw_zklend, 3, 'zkLend Withdraw', 0, []),
    withdraw_native_bridge              : (withdraw_native_bridge, 3, 'Native Bridge Withdraw', 0, []),
    collector_eth                       : (collector_eth, 4, 'Collect ETH from tokens', 0, []),
    okx_deposit                         : (okx_deposit, 5, 'OKX Deposit', 0, []),
    bingx_deposit                       : (bingx_deposit, 5, 'Bingx Deposit', 0, []),
    binance_deposit                     : (binance_deposit, 5, 'Binance Deposit', 0, []),
}


def get_func_by_name(module_name, help_message:bool = False):
    for k, v in AVAILABLE_MODULES_INFO.items():
        if k.__name__ == module_name:
            if help_message:
                return v[2]
            return v[0]


class RouteGenerator(Logger):
    def __init__(self, silent:bool = True):
        Logger.__init__(self)
        if GOOGLE_SHEET_URL != '' and not silent:
            self.gc: Client = service_account(filename=GSHEET_CONFIG)
            self.sh: Spreadsheet = self.gc.open_by_url(GOOGLE_SHEET_URL)
            self.ws: Worksheet = self.sh.worksheet(GOOGLE_SHEET_PAGE_NAME)
        else:
            self.gc, self.sh, self.ws = None, None, None
        self.w3 = AsyncWeb3()
        if GLOBAL_NETWORK == 9:
            map_data = {
                'mySwap Swap': swap_myswap,
                'Jediswap Swap': swap_jediswap,
                '10kSwap Swap': swap_10kswap,
                'SithSwap Swap': swap_sithswap,
                'Protoss Swap': swap_protoss,
                'Avnu Swap': swap_avnu,
                'zkLend Deposit': deposit_zklend,
                'Nostra Deposit': deposit_nostra,
                'Mint Starknet ID': mint_starknet_identity,
                'Mint StarkStars': mint_starkstars,
            }
        else:
            self.logger_msg(None, None,
                            msg=f"This network does not support in Google SpreadSheets", type_msg='error')
            map_data = {}
        self.function_mappings = map_data

    @staticmethod
    def classic_generate_route():
        route = []
        deposit_modules = [
            'deposit_basilisk',
            'deposit_eralend',
            'deposit_reactorfusion',
            'deposit_zerolend',
            'deposit_nostra',
            'deposit_zklend',
            'deposit_rocketsam',
            'deposit_layerbank',
        ]
        for i in CLASSIC_ROUTES_MODULES_USING:
            module_name = random.choice(i)
            if module_name is None:
                continue
            module = get_func_by_name(module_name)
            route.append(module.__name__)
            if CLASSIC_WITHDRAW_DEPENDENCIES and module_name in deposit_modules:
                withdraw_module_name = module_name.replace('deposit', 'withdraw')
                withdraw_module = get_func_by_name(withdraw_module_name)
                route.append(withdraw_module.__name__)
        return route

    def get_function_mappings_key(self, value):
        for key, val in self.function_mappings.items():
            if val == value:
                return key

    def get_account_name_list(self):
        try:
            return self.ws.col_values(1)[1:]
        except Exception as error:
            self.logger_msg(None, None, f"Put data into 'GOOGLE_SHEET_URL' and 'service_accounts.json' first!", 'error')
            raise SoftwareException(f"{error}")

    async def update_sheet(self, result_list: list, result_count: tuple):
        batch_size = 200
        for i in range(0, len(result_list), batch_size):
            batch_results = result_list[i:i + batch_size]
            total_results_to_update = []
            for item in batch_results:
                sheet_cell = rowcol_to_a1(row=item['row'], col=item['col'])
                total_results_to_update.append({
                    'range': sheet_cell,
                    'values': [[item['result']]],
                })
            self.ws.batch_update(total_results_to_update, value_input_option="USER_ENTERED")

        info = f'Google Sheet updated! Modules results info: ✅ - {result_count[0]} | ❌ - {result_count[1]}'
        self.logger_msg(None, None, info, 'success')
        return True

    def get_modules_list(self):
        modules_list_str = self.ws.row_values(1)[2:]

        modules_list = []
        for module in modules_list_str:
            if module in self.function_mappings:
                modules_list.append(self.function_mappings[module])
        return modules_list

    def get_data_for_batch(self, account_names:list):
        wallet_list = self.get_account_name_list()
        batch_size = 200
        data_to_return = {}

        for i in range(0, len(account_names), batch_size):
            batch_account_names = account_names[i:i+batch_size]
            batch_data = self.get_data_for_single_batch(batch_account_names, wallet_list)
            data_to_return.update(batch_data)

        return data_to_return

    def get_data_for_single_batch(self, batch_account_names:list, wallet_list:list):
        ranges_for_sheet = []
        batch_data = {}
        data_to_return = {}
        col = 2 + len(self.function_mappings)

        for account_name in batch_account_names:
            row = 2 + wallet_list.index(account_name)
            batch_data[row] = {
                'account_name': account_name
            }
            sheet_range = f"{rowcol_to_a1(row=row, col=3)}:{rowcol_to_a1(row=row, col=col)}"
            ranges_for_sheet.append(sheet_range)

        full_data = self.ws.batch_get(ranges_for_sheet)

        for index, data in enumerate(batch_data.items()):
            k, v = data
            data_to_return[v['account_name']] = {
                'progress': full_data[index]
            }

        return data_to_return

    async def get_smart_routes_for_batch(self, accounts_names:list):
        batch_data = self.get_data_for_batch(accounts_names)
        modules_list = self.get_modules_list()
        tasks = []
        for accounts_names in accounts_names:
            tasks.append(self.get_smart_route(accounts_names, batch_data[accounts_names]['progress'][0],
                         batch_mode=True, modules_list=modules_list))
        await asyncio.gather(*tasks)

    async def get_smart_route(self, account_name: str, wallet_statuses:list = None,
                              batch_mode:bool = False, modules_list:list = None):
        if not batch_mode:
            wallets_list = self.get_account_name_list()
            modules_list = self.get_modules_list()

            wallet_modules_statuses = self.ws.row_values(wallets_list.index(account_name) + 2)[2:]
        else:
            wallet_modules_statuses = wallet_statuses

        modules_to_work = []
        collaterals_modules = []
        transfers_modules = [transfer_eth_to_myself, transfer_eth]

        for i in range(len(wallet_modules_statuses)):
            if wallet_modules_statuses[i] in ["Not Started", "Error"]:
                path = list(self.function_mappings.keys())[i]
                modules_to_work.append([modules_list[i], path])

        excluded_modules = [get_func_by_name(module) for module in EXCLUDED_MODULES
                            if get_func_by_name(module) in list(self.function_mappings.values())]

        possible_modules = [module for module in modules_to_work if module not in excluded_modules]

        want_count = len(modules_to_work) if ALL_MODULES_TO_RUN else random.choice(MODULES_COUNT)
        possible_count = min(want_count, len(possible_modules))

        possible_modules_data = [AVAILABLE_MODULES_INFO[module] for module in possible_modules]

        smart_route: list = random.sample(possible_modules_data, possible_count)

        if DMAIL_IN_ROUTES:
            smart_route.extend([AVAILABLE_MODULES_INFO[send_message_dmail] for _ in range(random.choice(DMAIL_COUNT))])

        if COLLATERAL_IN_ROUTES and collaterals_modules:
            smart_route.extend([AVAILABLE_MODULES_INFO[random.choice(collaterals_modules)]
                                for _ in range(random.choice(COLLATERAL_COUNT))])

        if TRANSFER_IN_ROUTES and transfers_modules:
            smart_route.extend([AVAILABLE_MODULES_INFO[random.choice(transfers_modules)]
                                for _ in range(random.choice(TRANSFER_COUNT))])

        if WITHDRAW_LANDING:
            if GLOBAL_NETWORK == 9:
                smart_route.append(AVAILABLE_MODULES_INFO[withdraw_zklend])
                smart_route.append(AVAILABLE_MODULES_INFO[withdraw_nostra])

        bridge_modules = [AVAILABLE_MODULES_INFO[bridge_rhino] if HELPERS_CONFIG['bridge_rhino'] else None,
                          AVAILABLE_MODULES_INFO[bridge_layerswap] if HELPERS_CONFIG['bridge_layerswap'] else None,
                          AVAILABLE_MODULES_INFO[bridge_orbiter] if HELPERS_CONFIG['bridge_orbiter'] else None,
                          AVAILABLE_MODULES_INFO[bridge_native] if HELPERS_CONFIG['bridge_native'] else None]

        bridge_to_add = [i for i in bridge_modules if i]

        if bridge_to_add:
            smart_route.append(random.choice(bridge_to_add))

        smart_route.append(AVAILABLE_MODULES_INFO[okx_withdraw] if HELPERS_CONFIG['okx_withdraw'] else None)
        smart_route.append(AVAILABLE_MODULES_INFO[bingx_withdraw] if HELPERS_CONFIG['bingx_withdraw'] else None)
        smart_route.append(AVAILABLE_MODULES_INFO[binance_withdraw] if HELPERS_CONFIG['binance_withdraw'] else None)
        smart_route.append(AVAILABLE_MODULES_INFO[okx_deposit] if HELPERS_CONFIG['okx_deposit'] else None)
        smart_route.append(AVAILABLE_MODULES_INFO[collector_eth] if HELPERS_CONFIG['collector_eth'] else None)
        smart_route.append(
            AVAILABLE_MODULES_INFO[make_balance_to_average] if HELPERS_CONFIG['make_balance_to_average'] else None)
        smart_route.append(
            AVAILABLE_MODULES_INFO[upgrade_stark_wallet] if HELPERS_CONFIG['upgrade_stark_wallet'] else None)
        smart_route.append(
            AVAILABLE_MODULES_INFO[deploy_stark_wallet] if HELPERS_CONFIG['deploy_stark_wallet'] else None)

        random.shuffle(smart_route)

        smart_route_with_priority = [(i[0][0].__name__, i[1]) if GLOBAL_NETWORK == 0 else i[0].__name__
                                     for i in sorted(list(filter(None, smart_route)), key=lambda x: x[1])]

        self.smart_routes_json_save(account_name, smart_route_with_priority)

    def classic_routes_json_save(self):
        clean_progress_file()
        with open('./data/services/wallets_progress.json', 'w') as file:
            accounts_data = {}
            for account_name in ACCOUNT_NAMES:
                if isinstance(account_name, (str, int)):
                    classic_route = self.classic_generate_route()
                    if SHUFFLE_ROUTE:
                        random.shuffle(classic_route)
                    account_data = {
                        "current_step": 0,
                        "route": classic_route
                    }
                    accounts_data[str(account_name)] = account_data
            json.dump(accounts_data, file, indent=4)
        self.logger_msg(
            None, None,
            f'Successfully generated {len(accounts_data)} classic routes in data/services/wallets_progress.json\n',
            'success')

    def smart_routes_json_save(self, account_name: str, route: list):
        progress_file_path = './data/services/wallets_progress.json'

        if SHUFFLE_ROUTE:
            random.shuffle(route)

        try:
            with open(progress_file_path, 'r+') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = {}

        data[account_name] = {
            "current_step": 0,
            "route": ([" ".join(item) for item in route] if isinstance(route[0], tuple) else route) if route else []
        }

        with open(progress_file_path, 'w') as file:
            json.dump(data, file, indent=4)

        self.logger_msg(
            None, None,
            f'Successfully generated smart routes for {account_name}', 'success')