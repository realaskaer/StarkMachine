"""
----------------------------------------------------CEX CONTROL---------------------------------------------------------
    Выберите сети/суммы для вывода и ввода с CEX. Не забудьте вставить API ключи в general_settings.py.

    1  - ETH-ERC20                10  - BNB-OPBNB           18 - MATIC-Polygon          27 - USDC-Optimism
    2  - ETH-Arbitrum One         11 - CELO-CELO            19 - USDT-Arbitrum One      28 - USDC-Polygon
    3  - ETH-Optimism             12 - GLMR-Moonbeam        20 - USDT-Avalanche         29 - USDC-Optimism (Bridged)
    4  - ETH-Starknet             13 - MOVR-Moonriver       21 - USDT-Optimism          30 - USDC-Polygon (Bridged)
    5  - ETH-zkSync Era           14 - METIS-Metis          22 - USDT-Polygon           31 - USDC-BSC
    6  - ETH-Linea                15 - CORE-CORE            23 - USDT-BSC               32 - USDC-ERC20
    7  - ETH-Base                 16 - CFX-CFX_EVM          24 - USDT-ERC20
    8  - AVAX-Avalanche C-Chain   17 - KLAY-Klaytn          25 - USDC-Arbitrum One
    9  - BNB-BSC                  18 - FTM-Fantom           26 - USDC-Avalanche C-Chain

    CEX_DEPOSIT_LIMITER | Настройка лимитного вывода на биржу. Указывать в $USD
                          1 значение - это минимальный баланс на аккаунте, чтобы софт начал процесс вывода
                          2 значение - это мин. и макс. сумма, которая должна остаться на балансе после вывода.

    CEX_BALANCE_WANTED | Софт выведет средства с биржи таким образом, чтобы уровнять баланс аккаунта к этой настройке.
                         Модуль (make_balance_to_average). Указывать в токенах, которые собираетесь заводить на кошельки

"""
'--------------------------------------------------------OKX-----------------------------------------------------------'

OKX_WITHDRAW_DATA = [
    [[17, (1, 1.1)], [18, (1, 1.1)]],  # Пример установки двух сетей
    [3, (0.001, 0.002)],
]

OKX_DEPOSIT_DATA = [
    [[17, (1, 1.011)], None],    # Пример установки None, для случайного выбора (выполнение действия или его пропуск)
    [(2, 3, 4), (0.001, 0.002)]  # Пример указания нескольких сетей, cофт выберет сеть с наибольшим балансом
]

'--------------------------------------------------------BingX---------------------------------------------------------'

BINGX_WITHDRAW_DATA = [
    [17, (1, 1.011)],
]

BINGX_DEPOSIT_DATA = [
    [17, (1, 1.011)],
]

'-------------------------------------------------------Binance--------------------------------------------------------'

BINANCE_WITHDRAW_DATA = [
    [17, (1, 1.011)],
]

BINANCE_DEPOSIT_DATA = [
    [17, (1, 1.011)],
]

'-------------------------------------------------------Control--------------------------------------------------------'

CEX_DEPOSIT_LIMITER = 1, (1, 10000)  # (Ограничитель баланса, (мин. сумма, макс. сумма для остатка на балансе))
CEX_BALANCE_WANTED = 0.01               # Необходимый баланс на аккаунтах для уравнителя (make_balance_to_average)

"""
------------------------------------------------BRIDGE CONTROL----------------------------------------------------------
    Проверьте руками, работает ли сеть на сайте. (Софт сам проверит, но зачем его напрягать?)
    Не забудьте вставить API ключ для LayerSwap. Для каждого моста поддерживается уникальная настройка
    
    Можно указать минимальную/максимальную сумму или минимальный/максимальный % от баланса
    
    Количество - (0.01, 0.02)
    Процент    - ("10", "20") ⚠️ Значения в скобках
       
        Arbitrum = 1                    Polygon ZKEVM = 10 
        Arbitrum Nova = 2               zkSync Era = 11     
        Base = 3                       *Zora = 12 
        Linea = 4                       Ethereum = 13
        Manta = 5                      *Avalanche = 14
       *Polygon = 6                     BNB Chain = 15
        Optimism = 7                 (O)Metis = 26        
        Scroll = 8                     *OpBNB = 28
        Starknet = 9                   *Mantle = 29
                                        ZKFair = 45   
    
    * - не поддерживается в Rhino.fi
    (A) - сети, поддерживаемые Across мостом
    (0) - поддерживается только для Orbiter моста
    NATIVE_CHAIN_ID_FROM(TO) = [2, 4, 16] | Одна из сетей будет выбрана
    NATIVE_WITHDRAW_AMOUNT | Настройка для вывода из нативного моста (withdraw_native_bridge)
    BRIDGE_AMOUNT_LIMITER | Настройка лимитных бриджей. Указывать в $USD
                            1 значение - это минимальный баланс на аккаунте, чтобы софт начал процесс бриджа
                            2 значение - это мин. и макс. сумма, которая должна остаться на балансе после бриджа
"""
NATIVE_CHAIN_ID_FROM = [13]                # Исходящая сеть. 21.01.2024 Применимо только для bridge_zora
NATIVE_CHAIN_ID_TO = [11]                  # Входящая сеть. 21.01.2024 Применимо только для bridge_zora
NATIVE_BRIDGE_AMOUNT = (0.002, 0.002)     # (минимум, максимум) (% или кол-во)
NATIVE_WITHDRAW_AMOUNT = (0.0001, 0.0002)   # (минимум, максимум) (% или кол-во)

ORBITER_CHAIN_ID_FROM = [1, 2, 3, 7]       # Исходящая сеть
ORBITER_CHAIN_ID_TO = [11]                 # Входящая сеть
ORBITER_BRIDGE_AMOUNT = (0.003, 0.004)    # (минимум, максимум) (% или кол-во)
ORBITER_TOKEN_NAME = 'ETH'

LAYERSWAP_CHAIN_ID_FROM = [1]               # Исходящая сеть
LAYERSWAP_CHAIN_ID_TO = [4]                 # Входящая сеть
LAYERSWAP_BRIDGE_AMOUNT = (0.002, 0.002)    # (минимум, максимум) (% или кол-во)
LAYERSWAP_TOKEN_NAME = 'ETH'

RHINO_CHAIN_ID_FROM = [1]                # Исходящая сеть
RHINO_CHAIN_ID_TO = [11]                 # Входящая сеть
RHINO_BRIDGE_AMOUNT = (0.012, 0.022)     # (минимум, максимум) (% или кол-во)

BRIDGE_AMOUNT_LIMITER = 1, (1, 10000)  # (Ограничитель баланса, (мин. сумма, макс. сумма для остатка на балансе))

"""
--------------------------------------------------OTHER SETTINGS--------------------------------------------------------

    STARKSTARS_NFT_CONTRACTS | Укажите какие NFT ID будут участвовать в минте. Все что в скобках, будут использованы
    NEW_WALLET_TYPE | Определяет какой кошелек будет задеплоен, если вы решили создать новый. 0 - ArgentX | 1 - Braavos
"""

STARKSTARS_NFT_CONTRACTS = (1, 2, 3, 4)  # при (0) заминтит случайную новую NFT
NEW_WALLET_TYPE = 1

"""
----------------------------------------------GOOGLE-ROUTES CONTROL-----------------------------------------------------
    Технология сохранения прогресса для каждого аккаунта с помощью Google Spreadsheets 
    При каждом запуске, софт будет брать информацию из Google таблицы и настроек снизу, для генерации уникального
     маршрута под каждый аккаунт в таблице.  
    ⚠️Количество аккаунтов и их расположение должно быть строго одинаковым для вашего Excel и Google Spreadsheets⚠️
                                                         
    DEPOSIT_CONFIG | Включает в маршрут для каждого аккаунта модули, со значениями '1'
                     'okx_withdraw' всегда будет первой
                     Бриджи всегда после 'okx_withdraw'
                     'okx_deposit' и 'okx_collect_from_sub' всегда последние
    
"""

DMAIL_IN_ROUTES = False        # True или False | Включает Dmail в маршрут
TRANSFER_IN_ROUTES = False     # True или False | Включает трансферы в маршрут
COLLATERAL_IN_ROUTES = False   # True или False | Включает случайное вкл/выкл страховки в маршрут

DMAIL_COUNT = (1, 1)          # (минимум, максимум) дополнительных транзакций для Dmail
TRANSFER_COUNT = (1, 2)       # (минимум, максимум) дополнительных транзакций для трансферов
COLLATERAL_COUNT = (1, 2)     # (минимум, максимум) дополнительных транзакций для вкл/выкл страхования

MODULES_COUNT = (1, 1)         # (минимум, максимум) неотработанных модулей из Google таблицы
ALL_MODULES_TO_RUN = False     # True или False | Включает все неотработанные модули в маршрут
WITHDRAW_LP = False            # True или False | Включает в маршрут все модули для вывода ликвидности из DEX
WITHDRAW_LANDING = False       # True или False | Включает в маршрут все модули для вывода ликвидности из лендингов
HELP_NEW_MODULE = False        # True или False | Добавляет случайный модуль при неудачном выполнении модуля из маршрута
EXCLUDED_MODULES = ['swap_openocean']  # Исключает выбранные модули из маршрута. Список в Classic-Routes

HELPERS_CONFIG = {
    'okx_withdraw'                        : 0,  # смотри CEX CONTROL
    'bingx_withdraw'                      : 0,  # смотри CEX CONTROL
    'binance_withdraw'                    : 0,  # смотри CEX CONTROL
    'collector_eth'                       : 0,  # сбор всех токенов в ETH внутри сети GLOBAL_NETWORK
    'make_balance_to_average'             : 0,  # уравнивает ваши балансы на аккаунтах (см. инструкцию к софту)
    'upgrade_stark_wallet'                : 0,  # обновляет кошелек, во время маршрута
    'deploy_stark_wallet'                 : 0,  # деплоит кошелек, после вывода с OKX
    'bridge_rhino'                        : 0,  # смотри BRIDGE CONTROL
    'bridge_layerswap'                    : 0,  # смотри BRIDGE CONTROL
    'bridge_orbiter'                      : 0,  # смотри BRIDGE CONTROL
    'bridge_native'                       : 0,  # смотри BRIDGE CONTROL
    'okx_deposit'                         : 0,  # ввод средств на биржу
}

"""
--------------------------------------------CLASSIC-ROUTES CONTROL------------------------------------------------------

---------------------------------------------------HELPERS--------------------------------------------------------------        

    okx_withdraw                     # смотри CEX CONTROL
    bingx_withdraw                   # смотри CEX CONTROL
    binance_withdraw                 # смотри CEX CONTROL
    
    random_okx_withdraw              # вывод в рандомную сеть из OKX_MULTI_WITHDRAW
    random_bingx_withdraw            # вывод в рандомную сеть из BINGX_MULTI_WITHDRAW
    random_binance_withdraw          # вывод в рандомную сеть из BINANCE_MULTI_WITHDRAW
    
    collector_eth                    # сбор всех токенов в ETH
    make_balance_to_average          # уравнивает ваши балансы на аккаунтах (см. CEX_BALANCE_WANTED) 
    upgrade_stark_wallet             # обновляет кошелек, во время маршрута
    deploy_stark_wallet              # деплоит кошелек, после вывода с OKX
    
    bridge_layerswap                 # смотри BRIDGE CONTROL
    bridge_orbiter                   # смотри BRIDGE CONTROL
    bridge_rhino                     # смотри BRIDGE CONTROL
    bridge_native                    # смотри BRIDGE CONTROL (кол-во из NATIVE_DEPOSIT_AMOUNT) 
    
    okx_deposit                      # ввод средств на биржу + сбор средств на субАккаунтов на основной счет
    bingx_deposit                    # ввод средств на биржу 
    binance_deposit                  # ввод средств на биржу + сбор средств на субАккаунтов на основной счет
    
----------------------------------------------------STARKNET------------------------------------------------------------        
    
    upgrade_stark_wallet            
    deploy_stark_wallet     
    deposit_nostra                 
    deposit_zklend                 
    swap_jediswap                   
    swap_avnu
    swap_10kswap
    swap_sithswap
    swap_protoss
    swap_myswap
    send_message_dmail
    random_approve
    transfer_eth                     
    transfer_eth_to_myself                        
    enable_collateral_zklend
    disable_collateral_zklend
    mint_starknet_identity
    mint_starkstars
    withdraw_nostra
    withdraw_zklend
    withdraw_native_bridge
    
    Роуты для настоящих древлян (Машина - зло).
    Выберите необходимые модули для взаимодействия
    Вы можете создать любой маршрут, софт отработает строго по нему. Для каждого списка будет выбран один модуль в
    маршрут, если софт выберет None, то он пропустит данный список модулей. 
    Список модулей сверху.
    
    CLASSIC_ROUTES_MODULES_USING = [
        ['okx_withdraw'],
        ['bridge_layerswap', 'bridge_native'],
        ['swap_10kswap', 'swap_avnu', 'swap_jediswap', None],
        ...
    ]
"""

CLASSIC_WITHDRAW_DEPENDENCIES = False  # при True после каждого модуля на добавление ликвы в лендинг, будет ее выводить

CLASSIC_ROUTES_MODULES_USING = [
    ['okx_withdraw'],
    ['bridge_layerswap', 'bridge_native'],
    ['swap_10kswap', 'swap_avnu', 'swap_jediswap', None],
]
