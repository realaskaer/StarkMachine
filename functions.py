import random

from modules import *
from utils.networks import *
from general_settings import GLOBAL_NETWORK
from settings import (ORBITER_CHAIN_ID_FROM, LAYERSWAP_CHAIN_ID_FROM, RHINO_CHAIN_ID_FROM)


def get_client(account_name, private_key, network, proxy, bridge_from_evm:bool = False) -> Client | StarknetClient:
    if GLOBAL_NETWORK != 9 or bridge_from_evm:
        return Client(account_name, private_key, network, proxy)
    return StarknetClient(account_name, private_key, network, proxy)


def get_interface_by_chain_id(chain_id, deposit_module:bool = False):
    return {
        9: StarknetEVM if deposit_module else Starknet,
    }[chain_id]


def get_network_by_chain_id(chain_id):
    return {
        0: ArbitrumRPC,
        1: ArbitrumRPC,
        2: Arbitrum_novaRPC,
        3: BaseRPC,
        4: LineaRPC,
        5: MantaRPC,
        6: PolygonRPC,
        7: OptimismRPC,
        8: ScrollRPC,
        9: StarknetRPC,
        10: Polygon_ZKEVM_RPC,
        11: zkSyncEraRPC,
        12: ZoraRPC,
        13: EthereumRPC,
        14: AvalancheRPC,
        15: BSC_RPC,
    }[chain_id]


def get_key_by_id_from(args, chain_from_id):
    private_keys = args[0].get('stark_key'), args[0].get('evm_key')
    current_key = private_keys[1]
    if chain_from_id == 9:
        current_key = private_keys[0]
    return current_key


async def cex_deposit_util(current_client, dapp_id:int, deposit_data:tuple):
    class_name = {
        1: OKX,
        2: BingX,
        3: Binance
    }[dapp_id]

    return await class_name(current_client).deposit(deposit_data=deposit_data)


async def okx_deposit(account_name, private_key, network, proxy):
    worker = Custom(get_client(account_name, private_key, network, proxy))
    return await worker.smart_cex_deposit(dapp_id=1)


async def bingx_deposit(account_name, private_key, network, proxy):
    worker = Custom(get_client(account_name, private_key, network, proxy))
    return await worker.smart_cex_deposit(dapp_id=2)


async def binance_deposit(account_name, private_key, network, proxy):
    worker = Custom(get_client(account_name, private_key, network, proxy))
    return await worker.smart_cex_deposit(dapp_id=3)


async def bridge_utils(current_client, dapp_id,  chain_from_id, bridge_data, private_keys, need_fee=False):

    class_bridge = {
        1: LayerSwap,
        2: Orbiter,
        3: Rhino,
    }[dapp_id]

    network = get_network_by_chain_id(chain_from_id)
    bridge_from_evm = True if chain_from_id != 9 else False
    private_key = get_key_by_id_from(private_keys, chain_from_id)
    current_client = current_client if bridge_from_evm else get_client(
        current_client.account_name, private_key, network, current_client.proxy_init
    )

    return await class_bridge(current_client).bridge(
        chain_from_id, bridge_data=bridge_data, private_keys=private_keys, need_fee=need_fee
    )


async def bridge_layerswap(account_name, private_key, network, proxy, private_keys:dict = None):
    worker = Custom(get_client(account_name, private_key, network, proxy))
    return await worker.smart_bridge(dapp_id=1, private_keys=private_keys)


async def bridge_orbiter(account_name, private_key, network, proxy, private_keys:dict = None):
    worker = Custom(get_client(account_name, private_key, network, proxy))
    return await worker.smart_bridge(dapp_id=2, private_keys=private_keys)


async def bridge_rhino(account_name, private_key, network, proxy, private_keys:dict = None):
    worker = Custom(get_client(account_name, private_key, network, proxy))
    return await worker.smart_bridge(dapp_id=3, private_keys=private_keys)


async def send_message_dmail(account_name, private_key, _, proxy):
    network = get_network_by_chain_id(GLOBAL_NETWORK)
    worker = Dmail(get_client(account_name, private_key, network, proxy))
    return await worker.send_message()


async def bridge_native(account_name, _, __, proxy, *args, **kwargs):
    network = get_network_by_chain_id(13)

    blockchain = get_interface_by_chain_id(GLOBAL_NETWORK, deposit_module=True)
    bridge_from_evm = True if GLOBAL_NETWORK == 9 else False
    private_key = get_key_by_id_from(args, 13)

    worker = blockchain(get_client(account_name, private_key, network, proxy, bridge_from_evm))
    return await worker.deposit(*args, **kwargs)


async def transfer_eth(account_name, private_key, network, proxy):
    blockchain = get_interface_by_chain_id(GLOBAL_NETWORK)

    worker = blockchain(get_client(account_name, private_key, network, proxy))
    return await worker.transfer_eth()


async def transfer_eth_to_myself(account_name, private_key, network, proxy):
    blockchain = get_interface_by_chain_id(GLOBAL_NETWORK)

    worker = blockchain(get_client(account_name, private_key, network, proxy))
    return await worker.transfer_eth_to_myself()


async def withdraw_native_bridge(account_name, _, __, proxy, *args, **kwargs):
    blockchain = get_interface_by_chain_id(GLOBAL_NETWORK)
    network = get_network_by_chain_id(GLOBAL_NETWORK)
    private_key = get_key_by_id_from(args, GLOBAL_NETWORK)

    worker = blockchain(get_client(account_name, private_key, network, proxy))
    return await worker.withdraw(*args, **kwargs)


# async  def mint_deployed_token(account_name, private_key, network, proxy, *args, **kwargs):
#     mint = ZkSync(account_name, private_key, network, proxy)
#     await mint.mint_token()


async def swap_rango(account_name, private_key, network, proxy, **kwargs):
    worker = Rango(get_client(account_name, private_key, network, proxy))
    return await worker.swap(**kwargs)


async def swap_jediswap(account_name, private_key, network, proxy, *args, **kwargs):
    worker = JediSwap(get_client(account_name, private_key, network, proxy))
    return await worker.swap(*args, **kwargs)


async def swap_avnu(account_name, private_key, network, proxy, **kwargs):
    worker = AVNU(get_client(account_name, private_key, network, proxy))
    return await worker.swap(**kwargs)


async def swap_10kswap(account_name, private_key, network, proxy):
    worker = TenkSwap(get_client(account_name, private_key, network, proxy))
    return await worker.swap()


async def swap_sithswap(account_name, private_key, network, proxy):
    worker = SithSwap(get_client(account_name, private_key, network, proxy))
    return await worker.swap()


async def swap_myswap(account_name, private_key, network, proxy):
    worker = MySwap(get_client(account_name, private_key, network, proxy))
    return await worker.swap()


async def swap_protoss(account_name, private_key, network, proxy):
    worker = Protoss(get_client(account_name, private_key, network, proxy))
    return await worker.swap()


async def deploy_stark_wallet(account_name, private_key, network, proxy):
    worker = Starknet(get_client(account_name, private_key, network, proxy))
    return await worker.deploy_wallet()


async def upgrade_stark_wallet(account_name, private_key, network, proxy):
    worker = Starknet(get_client(account_name, private_key, network, proxy))
    return await worker.upgrade_wallet()


async def mint_starknet_identity(account_name, private_key, network, proxy):
    worker = StarknetId(get_client(account_name, private_key, network, proxy))
    return await worker.mint()


async def mint_starkstars(account_name, private_key, network, proxy):
    worker = StarkStars(get_client(account_name, private_key, network, proxy))
    return await worker.mint()


# async def deposit_carmine(account_name, private_key, network, proxy):
#     worker = Carmine(get_client(account_name, private_key, network, proxy))
#     return await worker.deposit()
#
#
# async def withdraw_carmine(account_name, private_key, network, proxy):
#     worker = Carmine(get_client(account_name, private_key, network, proxy))
#     return await worker.withdraw()


async def deposit_nostra(account_name, private_key, network, proxy):
    worker = Nostra(get_client(account_name, private_key, network, proxy))
    return await worker.deposit()


async def withdraw_nostra(account_name, private_key, network, proxy):
    worker = Nostra(get_client(account_name, private_key, network, proxy))
    return await worker.withdraw()


async def deposit_zklend(account_name, private_key, network, proxy):
    worker = ZkLend(get_client(account_name, private_key, network, proxy))
    return await worker.deposit()


async def withdraw_zklend(account_name, private_key, network, proxy):
    worker = ZkLend(get_client(account_name, private_key, network, proxy))
    return await worker.withdraw()


async def enable_collateral_zklend(account_name, private_key, network, proxy):
    worker = ZkLend(get_client(account_name, private_key, network, proxy))
    return await worker.enable_collateral()


async def disable_collateral_zklend(account_name, private_key, network, proxy):
    worker = ZkLend(get_client(account_name, private_key, network, proxy))
    return await worker.disable_collateral()


async def random_approve(account_nameaccount_name, private_key, network, proxy):
    blockchain = get_interface_by_chain_id(GLOBAL_NETWORK)

    worker = blockchain(get_client(account_nameaccount_name, private_key, network, proxy))
    return await worker.random_approve()


async def collector_eth(account_name, private_key, network, proxy):

    worker = Custom(get_client(account_name, private_key, network, proxy))
    return await worker.collect_eth()


async def make_balance_to_average(account_name, private_key, network, proxy):

    worker = Custom(get_client(account_name, private_key, network, proxy))
    return await worker.balance_average()


async def okx_withdraw(account_name, private_key, network, proxy, *args, **kwargs):
    worker = OKX(get_client(account_name, private_key, network, proxy))
    return await worker.withdraw(*args, **kwargs)


async def bingx_withdraw(account_name, private_key, network, proxy, **kwargs):
    worker = BingX(get_client(account_name, private_key, network, proxy))
    return await worker.withdraw(**kwargs)


async def binance_withdraw(account_name, private_key, network, proxy, **kwargs):
    worker = Binance(get_client(account_name, private_key, network, proxy))
    return await worker.withdraw(**kwargs)
