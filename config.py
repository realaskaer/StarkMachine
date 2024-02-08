import asyncio
from utils.tools import get_accounts_data, get_eth_price

DMAIL_ABI = [{'inputs': [], 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'address', 'name': 'previousAdmin', 'type': 'address'}, {'indexed': False, 'internalType': 'address', 'name': 'newAdmin', 'type': 'address'}], 'name': 'AdminChanged', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'owner', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}], 'name': 'Approval', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'beacon', 'type': 'address'}], 'name': 'BeaconUpgraded', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'uint8', 'name': 'version', 'type': 'uint8'}], 'name': 'Initialized', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'from', 'type': 'address'}, {'indexed': True, 'internalType': 'string', 'name': 'to', 'type': 'string'}, {'indexed': True, 'internalType': 'string', 'name': 'path', 'type': 'string'}], 'name': 'Message', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'previousOwner', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'newOwner', 'type': 'address'}], 'name': 'OwnershipTransferred', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'address', 'name': 'account', 'type': 'address'}], 'name': 'Paused', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'from', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'to', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}], 'name': 'Transfer', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'address', 'name': 'account', 'type': 'address'}], 'name': 'Unpaused', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'implementation', 'type': 'address'}], 'name': 'Upgraded', 'type': 'event'}, {'inputs': [{'internalType': 'address', 'name': 'owner', 'type': 'address'}, {'internalType': 'address', 'name': 'spender', 'type': 'address'}], 'name': 'allowance', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}], 'name': 'approve', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'account', 'type': 'address'}], 'name': 'balanceOf', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}], 'name': 'burn', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'account', 'type': 'address'}, {'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}], 'name': 'burnFrom', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'decimals', 'outputs': [{'internalType': 'uint8', 'name': '', 'type': 'uint8'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'internalType': 'uint256', 'name': 'subtractedValue', 'type': 'uint256'}], 'name': 'decreaseAllowance', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'internalType': 'uint256', 'name': 'addedValue', 'type': 'uint256'}], 'name': 'increaseAllowance', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'initialize', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'to', 'type': 'address'}, {'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}], 'name': 'mint', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'name', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'owner', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'pause', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'paused', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'proxiableUUID', 'outputs': [{'internalType': 'bytes32', 'name': '', 'type': 'bytes32'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'renounceOwnership', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'string', 'name': 'to', 'type': 'string'}, {'internalType': 'string', 'name': 'path', 'type': 'string'}], 'name': 'send_mail', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'symbol', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'totalSupply', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'to', 'type': 'address'}, {'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}], 'name': 'transfer', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'from', 'type': 'address'}, {'internalType': 'address', 'name': 'to', 'type': 'address'}, {'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}], 'name': 'transferFrom', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'newOwner', 'type': 'address'}], 'name': 'transferOwnership', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'unpause', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'newImplementation', 'type': 'address'}], 'name': 'upgradeTo', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'newImplementation', 'type': 'address'}, {'internalType': 'bytes', 'name': 'data', 'type': 'bytes'}], 'name': 'upgradeToAndCall', 'outputs': [], 'stateMutability': 'payable', 'type': 'function'}]

ERC20_ABI = [{'inputs': [{'internalType': 'string', 'name': '_name', 'type': 'string'}, {'internalType': 'string', 'name': '_symbol', 'type': 'string'}, {'internalType': 'uint256', 'name': '_initialSupply', 'type': 'uint256'}], 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'owner', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}], 'name': 'Approval', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'from', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'to', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}], 'name': 'Transfer', 'type': 'event'}, {'inputs': [{'internalType': 'address', 'name': 'owner', 'type': 'address'}, {'internalType': 'address', 'name': 'spender', 'type': 'address'}], 'name': 'allowance', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}], 'name': 'approve', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'account', 'type': 'address'}], 'name': 'balanceOf', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'decimals', 'outputs': [{'internalType': 'uint8', 'name': '', 'type': 'uint8'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'internalType': 'uint256', 'name': 'subtractedValue', 'type': 'uint256'}], 'name': 'decreaseAllowance', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'internalType': 'uint256', 'name': 'addedValue', 'type': 'uint256'}], 'name': 'increaseAllowance', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'name', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint8', 'name': 'decimals_', 'type': 'uint8'}], 'name': 'setupDecimals', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'symbol', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'totalSupply', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'recipient', 'type': 'address'}, {'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}], 'name': 'transfer', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'sender', 'type': 'address'}, {'internalType': 'address', 'name': 'recipient', 'type': 'address'}, {'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}], 'name': 'transferFrom', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'nonpayable', 'type': 'function'}]

STARK_ERC20_ABI = [{'name': 'Uint256', 'size': 2, 'type': 'struct', 'members': [{'name': 'low', 'type': 'felt', 'offset': 0}, {'name': 'high', 'type': 'felt', 'offset': 1}]}, {'data': [{'name': 'from_', 'type': 'felt'}, {'name': 'to', 'type': 'felt'}, {'name': 'value', 'type': 'Uint256'}], 'keys': [], 'name': 'Transfer', 'type': 'event'}, {'data': [{'name': 'owner', 'type': 'felt'}, {'name': 'spender', 'type': 'felt'}, {'name': 'value', 'type': 'Uint256'}], 'keys': [], 'name': 'Approval', 'type': 'event'}, {'name': 'name', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'name', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'symbol', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'symbol', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'totalSupply', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'totalSupply', 'type': 'Uint256'}], 'stateMutability': 'view'}, {'name': 'decimals', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'decimals', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'balanceOf', 'type': 'function', 'inputs': [{'name': 'account', 'type': 'felt'}], 'outputs': [{'name': 'balance', 'type': 'Uint256'}], 'stateMutability': 'view'}, {'name': 'allowance', 'type': 'function', 'inputs': [{'name': 'owner', 'type': 'felt'}, {'name': 'spender', 'type': 'felt'}], 'outputs': [{'name': 'remaining', 'type': 'Uint256'}], 'stateMutability': 'view'}, {'name': 'permittedMinter', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'minter', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'initialized', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'res', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'get_version', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'version', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'get_identity', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'identity', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'initialize', 'type': 'function', 'inputs': [{'name': 'init_vector_len', 'type': 'felt'}, {'name': 'init_vector', 'type': 'felt*'}], 'outputs': []}, {'name': 'transfer', 'type': 'function', 'inputs': [{'name': 'recipient', 'type': 'felt'}, {'name': 'amount', 'type': 'Uint256'}], 'outputs': [{'name': 'success', 'type': 'felt'}]}, {'name': 'transferFrom', 'type': 'function', 'inputs': [{'name': 'sender', 'type': 'felt'}, {'name': 'recipient', 'type': 'felt'}, {'name': 'amount', 'type': 'Uint256'}], 'outputs': [{'name': 'success', 'type': 'felt'}]}, {'name': 'approve', 'type': 'function', 'inputs': [{'name': 'spender', 'type': 'felt'}, {'name': 'amount', 'type': 'Uint256'}], 'outputs': [{'name': 'success', 'type': 'felt'}]}, {'name': 'increaseAllowance', 'type': 'function', 'inputs': [{'name': 'spender', 'type': 'felt'}, {'name': 'added_value', 'type': 'Uint256'}], 'outputs': [{'name': 'success', 'type': 'felt'}]}, {'name': 'decreaseAllowance', 'type': 'function', 'inputs': [{'name': 'spender', 'type': 'felt'}, {'name': 'subtracted_value', 'type': 'Uint256'}], 'outputs': [{'name': 'success', 'type': 'felt'}]}, {'name': 'permissionedMint', 'type': 'function', 'inputs': [{'name': 'recipient', 'type': 'felt'}, {'name': 'amount', 'type': 'Uint256'}], 'outputs': []}, {'name': 'permissionedBurn', 'type': 'function', 'inputs': [{'name': 'account', 'type': 'felt'}, {'name': 'amount', 'type': 'Uint256'}], 'outputs': []}]

ORBITER_ABI = {
    'evm_contract': [{'inputs': [{'internalType': 'address payable', 'name': '_to', 'type': 'address'}, {'internalType': 'bytes', 'name': '_ext', 'type': 'bytes'}], 'name': 'transfer', 'outputs': [], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'contract IERC20', 'name': '_token', 'type': 'address'}, {'internalType': 'address', 'name': '_to', 'type': 'address'}, {'internalType': 'uint256', 'name': '_amount', 'type': 'uint256'}, {'internalType': 'bytes', 'name': '_ext', 'type': 'bytes'}], 'name': 'transferERC20', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}],
    'stark_contract': [{'name': 'Uint256', 'size': 2, 'type': 'struct', 'members': [{'name': 'low', 'type': 'felt', 'offset': 0}, {'name': 'high', 'type': 'felt', 'offset': 1}]}, {'name': 'transferERC20', 'type': 'function', 'inputs': [{'name': '_token', 'type': 'felt'}, {'name': '_to', 'type': 'felt'}, {'name': '_amount', 'type': 'Uint256'}, {'name': '_ext', 'type': 'felt'}], 'outputs': []}]
}

RHINO_ABI = {
    'nft_common': [{'inputs': [{'internalType': 'string', 'name': '_name', 'type': 'string'}, {'internalType': 'string', 'name': '_symbol', 'type': 'string'}, {'internalType': 'uint256', 'name': '_mintFee', 'type': 'uint256'}, {'internalType': 'string', 'name': '_tokenURI', 'type': 'string'}], 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'owner', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'approved', 'type': 'address'}, {'indexed': True, 'internalType': 'uint256', 'name': 'tokenId', 'type': 'uint256'}], 'name': 'Approval', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'owner', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'operator', 'type': 'address'}, {'indexed': False, 'internalType': 'bool', 'name': 'approved', 'type': 'bool'}], 'name': 'ApprovalForAll', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'previousOwner', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'newOwner', 'type': 'address'}], 'name': 'OwnershipTransferred', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'from', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'to', 'type': 'address'}, {'indexed': True, 'internalType': 'uint256', 'name': 'tokenId', 'type': 'uint256'}], 'name': 'Transfer', 'type': 'event'}, {'inputs': [{'internalType': 'address', 'name': 'to', 'type': 'address'}, {'internalType': 'uint256', 'name': 'tokenId', 'type': 'uint256'}], 'name': 'approve', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'owner', 'type': 'address'}], 'name': 'balanceOf', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'tokenId', 'type': 'uint256'}], 'name': 'getApproved', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'owner', 'type': 'address'}, {'internalType': 'address', 'name': 'operator', 'type': 'address'}], 'name': 'isApprovedForAll', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'mint', 'outputs': [], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [], 'name': 'mintFee', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'name', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'owner', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'tokenId', 'type': 'uint256'}], 'name': 'ownerOf', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'renounceOwnership', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'from', 'type': 'address'}, {'internalType': 'address', 'name': 'to', 'type': 'address'}, {'internalType': 'uint256', 'name': 'tokenId', 'type': 'uint256'}], 'name': 'safeTransferFrom', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'from', 'type': 'address'}, {'internalType': 'address', 'name': 'to', 'type': 'address'}, {'internalType': 'uint256', 'name': 'tokenId', 'type': 'uint256'}, {'internalType': 'bytes', 'name': '_data', 'type': 'bytes'}], 'name': 'safeTransferFrom', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'operator', 'type': 'address'}, {'internalType': 'bool', 'name': 'approved', 'type': 'bool'}], 'name': 'setApprovalForAll', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'bytes4', 'name': 'interfaceId', 'type': 'bytes4'}], 'name': 'supportsInterface', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'symbol', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'tokenURI', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'tokenId', 'type': 'uint256'}], 'name': 'tokenURI', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'from', 'type': 'address'}, {'internalType': 'address', 'name': 'to', 'type': 'address'}, {'internalType': 'uint256', 'name': 'tokenId', 'type': 'uint256'}], 'name': 'transferFrom', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'newOwner', 'type': 'address'}], 'name': 'transferOwnership', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': '_mintFee', 'type': 'uint256'}], 'name': 'updateMintFee', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'withdraw', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}],
    'nft_rare': [{'inputs': [{'internalType': 'string', 'name': '_name', 'type': 'string'}, {'internalType': 'string', 'name': '_symbol', 'type': 'string'}, {'internalType': 'string', 'name': '_tokenURI', 'type': 'string'}, {'internalType': 'address', 'name': '_signerAddress', 'type': 'address'}], 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'owner', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'approved', 'type': 'address'}, {'indexed': True, 'internalType': 'uint256', 'name': 'tokenId', 'type': 'uint256'}], 'name': 'Approval', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'owner', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'operator', 'type': 'address'}, {'indexed': False, 'internalType': 'bool', 'name': 'approved', 'type': 'bool'}], 'name': 'ApprovalForAll', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'previousOwner', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'newOwner', 'type': 'address'}], 'name': 'OwnershipTransferred', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'from', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'to', 'type': 'address'}, {'indexed': True, 'internalType': 'uint256', 'name': 'tokenId', 'type': 'uint256'}], 'name': 'Transfer', 'type': 'event'}, {'inputs': [{'internalType': 'address', 'name': 'to', 'type': 'address'}, {'internalType': 'uint256', 'name': 'tokenId', 'type': 'uint256'}], 'name': 'approve', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'owner', 'type': 'address'}], 'name': 'balanceOf', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'tokenId', 'type': 'uint256'}], 'name': 'getApproved', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'owner', 'type': 'address'}, {'internalType': 'address', 'name': 'operator', 'type': 'address'}], 'name': 'isApprovedForAll', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'masterSigner', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'messagePrefix', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'bytes', 'name': 'signature', 'type': 'bytes'}], 'name': 'mint', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'name': 'minters', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'name', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'owner', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'tokenId', 'type': 'uint256'}], 'name': 'ownerOf', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'renounceOwnership', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'from', 'type': 'address'}, {'internalType': 'address', 'name': 'to', 'type': 'address'}, {'internalType': 'uint256', 'name': 'tokenId', 'type': 'uint256'}], 'name': 'safeTransferFrom', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'from', 'type': 'address'}, {'internalType': 'address', 'name': 'to', 'type': 'address'}, {'internalType': 'uint256', 'name': 'tokenId', 'type': 'uint256'}, {'internalType': 'bytes', 'name': '_data', 'type': 'bytes'}], 'name': 'safeTransferFrom', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'operator', 'type': 'address'}, {'internalType': 'bool', 'name': 'approved', 'type': 'bool'}], 'name': 'setApprovalForAll', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'bytes4', 'name': 'interfaceId', 'type': 'bytes4'}], 'name': 'supportsInterface', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'symbol', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'tokenId', 'type': 'uint256'}], 'name': 'tokenURI', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'from', 'type': 'address'}, {'internalType': 'address', 'name': 'to', 'type': 'address'}, {'internalType': 'uint256', 'name': 'tokenId', 'type': 'uint256'}], 'name': 'transferFrom', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'newOwner', 'type': 'address'}], 'name': 'transferOwnership', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': '_masterSignerAddress', 'type': 'address'}], 'name': 'updateSignerAddress', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}]
}

STARKSTARS_ABI = [{'name': 'SRC5Impl', 'type': 'impl', 'interface_name': 'openzeppelin::introspection::interface::ISRC5'}, {'name': 'core::bool', 'type': 'enum', 'variants': [{'name': 'False', 'type': '()'}, {'name': 'True', 'type': '()'}]}, {'name': 'openzeppelin::introspection::interface::ISRC5', 'type': 'interface', 'items': [{'name': 'supports_interface', 'type': 'function', 'inputs': [{'name': 'interface_id', 'type': 'core::felt252'}], 'outputs': [{'type': 'core::bool'}], 'state_mutability': 'view'}]}, {'name': 'SRC5CamelImpl', 'type': 'impl', 'interface_name': 'openzeppelin::introspection::interface::ISRC5Camel'}, {'name': 'openzeppelin::introspection::interface::ISRC5Camel', 'type': 'interface', 'items': [{'name': 'supportsInterface', 'type': 'function', 'inputs': [{'name': 'interfaceId', 'type': 'core::felt252'}], 'outputs': [{'type': 'core::bool'}], 'state_mutability': 'view'}]}, {'name': 'ERC721MetadataImpl', 'type': 'impl', 'interface_name': 'openzeppelin::token::erc721::interface::IERC721Metadata'}, {'name': 'core::integer::u256', 'type': 'struct', 'members': [{'name': 'low', 'type': 'core::integer::u128'}, {'name': 'high', 'type': 'core::integer::u128'}]}, {'name': 'openzeppelin::token::erc721::interface::IERC721Metadata', 'type': 'interface', 'items': [{'name': 'name', 'type': 'function', 'inputs': [], 'outputs': [{'type': 'core::felt252'}], 'state_mutability': 'view'}, {'name': 'symbol', 'type': 'function', 'inputs': [], 'outputs': [{'type': 'core::felt252'}], 'state_mutability': 'view'}, {'name': 'token_uri', 'type': 'function', 'inputs': [{'name': 'token_id', 'type': 'core::integer::u256'}], 'outputs': [{'type': 'core::felt252'}], 'state_mutability': 'view'}]}, {'name': 'ERC721MetadataCamelOnlyImpl', 'type': 'impl', 'interface_name': 'openzeppelin::token::erc721::interface::IERC721MetadataCamelOnly'}, {'name': 'openzeppelin::token::erc721::interface::IERC721MetadataCamelOnly', 'type': 'interface', 'items': [{'name': 'tokenURI', 'type': 'function', 'inputs': [{'name': 'tokenId', 'type': 'core::integer::u256'}], 'outputs': [{'type': 'core::felt252'}], 'state_mutability': 'view'}]}, {'name': 'ERC721Impl', 'type': 'impl', 'interface_name': 'openzeppelin::token::erc721::interface::IERC721'}, {'name': 'core::array::Span::<core::felt252>', 'type': 'struct', 'members': [{'name': 'snapshot', 'type': '@core::array::Array::<core::felt252>'}]}, {'name': 'openzeppelin::token::erc721::interface::IERC721', 'type': 'interface', 'items': [{'name': 'balance_of', 'type': 'function', 'inputs': [{'name': 'account', 'type': 'core::starknet::contract_address::ContractAddress'}], 'outputs': [{'type': 'core::integer::u256'}], 'state_mutability': 'view'}, {'name': 'owner_of', 'type': 'function', 'inputs': [{'name': 'token_id', 'type': 'core::integer::u256'}], 'outputs': [{'type': 'core::starknet::contract_address::ContractAddress'}], 'state_mutability': 'view'}, {'name': 'transfer_from', 'type': 'function', 'inputs': [{'name': 'from', 'type': 'core::starknet::contract_address::ContractAddress'}, {'name': 'to', 'type': 'core::starknet::contract_address::ContractAddress'}, {'name': 'token_id', 'type': 'core::integer::u256'}], 'outputs': [], 'state_mutability': 'external'}, {'name': 'safe_transfer_from', 'type': 'function', 'inputs': [{'name': 'from', 'type': 'core::starknet::contract_address::ContractAddress'}, {'name': 'to', 'type': 'core::starknet::contract_address::ContractAddress'}, {'name': 'token_id', 'type': 'core::integer::u256'}, {'name': 'data', 'type': 'core::array::Span::<core::felt252>'}], 'outputs': [], 'state_mutability': 'external'}, {'name': 'approve', 'type': 'function', 'inputs': [{'name': 'to', 'type': 'core::starknet::contract_address::ContractAddress'}, {'name': 'token_id', 'type': 'core::integer::u256'}], 'outputs': [], 'state_mutability': 'external'}, {'name': 'set_approval_for_all', 'type': 'function', 'inputs': [{'name': 'operator', 'type': 'core::starknet::contract_address::ContractAddress'}, {'name': 'approved', 'type': 'core::bool'}], 'outputs': [], 'state_mutability': 'external'}, {'name': 'get_approved', 'type': 'function', 'inputs': [{'name': 'token_id', 'type': 'core::integer::u256'}], 'outputs': [{'type': 'core::starknet::contract_address::ContractAddress'}], 'state_mutability': 'view'}, {'name': 'is_approved_for_all', 'type': 'function', 'inputs': [{'name': 'owner', 'type': 'core::starknet::contract_address::ContractAddress'}, {'name': 'operator', 'type': 'core::starknet::contract_address::ContractAddress'}], 'outputs': [{'type': 'core::bool'}], 'state_mutability': 'view'}]}, {'name': 'ERC721CamelOnlyImpl', 'type': 'impl', 'interface_name': 'openzeppelin::token::erc721::interface::IERC721CamelOnly'}, {'name': 'openzeppelin::token::erc721::interface::IERC721CamelOnly', 'type': 'interface', 'items': [{'name': 'balanceOf', 'type': 'function', 'inputs': [{'name': 'account', 'type': 'core::starknet::contract_address::ContractAddress'}], 'outputs': [{'type': 'core::integer::u256'}], 'state_mutability': 'view'}, {'name': 'ownerOf', 'type': 'function', 'inputs': [{'name': 'tokenId', 'type': 'core::integer::u256'}], 'outputs': [{'type': 'core::starknet::contract_address::ContractAddress'}], 'state_mutability': 'view'}, {'name': 'transferFrom', 'type': 'function', 'inputs': [{'name': 'from', 'type': 'core::starknet::contract_address::ContractAddress'}, {'name': 'to', 'type': 'core::starknet::contract_address::ContractAddress'}, {'name': 'tokenId', 'type': 'core::integer::u256'}], 'outputs': [], 'state_mutability': 'external'}, {'name': 'safeTransferFrom', 'type': 'function', 'inputs': [{'name': 'from', 'type': 'core::starknet::contract_address::ContractAddress'}, {'name': 'to', 'type': 'core::starknet::contract_address::ContractAddress'}, {'name': 'tokenId', 'type': 'core::integer::u256'}, {'name': 'data', 'type': 'core::array::Span::<core::felt252>'}], 'outputs': [], 'state_mutability': 'external'}, {'name': 'setApprovalForAll', 'type': 'function', 'inputs': [{'name': 'operator', 'type': 'core::starknet::contract_address::ContractAddress'}, {'name': 'approved', 'type': 'core::bool'}], 'outputs': [], 'state_mutability': 'external'}, {'name': 'getApproved', 'type': 'function', 'inputs': [{'name': 'tokenId', 'type': 'core::integer::u256'}], 'outputs': [{'type': 'core::starknet::contract_address::ContractAddress'}], 'state_mutability': 'view'}, {'name': 'isApprovedForAll', 'type': 'function', 'inputs': [{'name': 'owner', 'type': 'core::starknet::contract_address::ContractAddress'}, {'name': 'operator', 'type': 'core::starknet::contract_address::ContractAddress'}], 'outputs': [{'type': 'core::bool'}], 'state_mutability': 'view'}]}, {'name': 'IStarkStarsImpl', 'type': 'impl', 'interface_name': 'achievments::contract::contract::IStarkStars'}, {'name': 'achievments::contract::contract::IStarkStars', 'type': 'interface', 'items': [{'name': 'get_price', 'type': 'function', 'inputs': [], 'outputs': [{'type': 'core::integer::u256'}], 'state_mutability': 'view'}, {'name': 'mint', 'type': 'function', 'inputs': [], 'outputs': [], 'state_mutability': 'external'}, {'name': 'withdraw', 'type': 'function', 'inputs': [], 'outputs': [], 'state_mutability': 'external'}, {'name': 'set_price', 'type': 'function', 'inputs': [{'name': 'price', 'type': 'core::integer::u256'}], 'outputs': [], 'state_mutability': 'external'}]}, {'name': 'constructor', 'type': 'constructor', 'inputs': [{'name': 'recipient', 'type': 'core::starknet::contract_address::ContractAddress'}, {'name': 'base_uri', 'type': 'core::felt252'}]}, {'kind': 'struct', 'name': 'achievments::contract::contract::Transfer', 'type': 'event', 'members': [{'kind': 'key', 'name': 'from', 'type': 'core::starknet::contract_address::ContractAddress'}, {'kind': 'key', 'name': 'to', 'type': 'core::starknet::contract_address::ContractAddress'}, {'kind': 'key', 'name': 'token_id', 'type': 'core::integer::u256'}]}, {'kind': 'struct', 'name': 'achievments::contract::contract::Approval', 'type': 'event', 'members': [{'kind': 'key', 'name': 'owner', 'type': 'core::starknet::contract_address::ContractAddress'}, {'kind': 'key', 'name': 'approved', 'type': 'core::starknet::contract_address::ContractAddress'}, {'kind': 'key', 'name': 'token_id', 'type': 'core::integer::u256'}]}, {'kind': 'struct', 'name': 'achievments::contract::contract::ApprovalForAll', 'type': 'event', 'members': [{'kind': 'key', 'name': 'owner', 'type': 'core::starknet::contract_address::ContractAddress'}, {'kind': 'key', 'name': 'operator', 'type': 'core::starknet::contract_address::ContractAddress'}, {'kind': 'data', 'name': 'approved', 'type': 'core::bool'}]}, {'kind': 'enum', 'name': 'achievments::contract::contract::Event', 'type': 'event', 'variants': [{'kind': 'nested', 'name': 'Transfer', 'type': 'achievments::contract::contract::Transfer'}, {'kind': 'nested', 'name': 'Approval', 'type': 'achievments::contract::contract::Approval'}, {'kind': 'nested', 'name': 'ApprovalForAll', 'type': 'achievments::contract::contract::ApprovalForAll'}]}]

WETH_ABI = [{'inputs': [], 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'owner', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}], 'name': 'Approval', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': '_account', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': '_amount', 'type': 'uint256'}], 'name': 'BridgeBurn', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'l1Token', 'type': 'address'}, {'indexed': False, 'internalType': 'string', 'name': 'name', 'type': 'string'}, {'indexed': False, 'internalType': 'string', 'name': 'symbol', 'type': 'string'}, {'indexed': False, 'internalType': 'uint8', 'name': 'decimals', 'type': 'uint8'}], 'name': 'BridgeInitialize', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': '_account', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': '_amount', 'type': 'uint256'}], 'name': 'BridgeMint', 'type': 'event'}, {'anonymous': False, 'inputs': [], 'name': 'EIP712DomainChanged', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'string', 'name': 'name', 'type': 'string'}, {'indexed': False, 'internalType': 'string', 'name': 'symbol', 'type': 'string'}, {'indexed': False, 'internalType': 'uint8', 'name': 'decimals', 'type': 'uint8'}], 'name': 'Initialize', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'uint8', 'name': 'version', 'type': 'uint8'}], 'name': 'Initialized', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'from', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'to', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}], 'name': 'Transfer', 'type': 'event'}, {'inputs': [], 'name': 'DOMAIN_SEPARATOR', 'outputs': [{'internalType': 'bytes32', 'name': '', 'type': 'bytes32'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'owner', 'type': 'address'}, {'internalType': 'address', 'name': 'spender', 'type': 'address'}], 'name': 'allowance', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}], 'name': 'approve', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'account', 'type': 'address'}], 'name': 'balanceOf', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': '_from', 'type': 'address'}, {'internalType': 'uint256', 'name': '_amount', 'type': 'uint256'}], 'name': 'bridgeBurn', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': '', 'type': 'address'}, {'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'name': 'bridgeMint', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'decimals', 'outputs': [{'internalType': 'uint8', 'name': '', 'type': 'uint8'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'internalType': 'uint256', 'name': 'subtractedValue', 'type': 'uint256'}], 'name': 'decreaseAllowance', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'deposit', 'outputs': [], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': '_to', 'type': 'address'}], 'name': 'depositTo', 'outputs': [], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [], 'name': 'eip712Domain', 'outputs': [{'internalType': 'bytes1', 'name': 'fields', 'type': 'bytes1'}, {'internalType': 'string', 'name': 'name', 'type': 'string'}, {'internalType': 'string', 'name': 'version', 'type': 'string'}, {'internalType': 'uint256', 'name': 'chainId', 'type': 'uint256'}, {'internalType': 'address', 'name': 'verifyingContract', 'type': 'address'}, {'internalType': 'bytes32', 'name': 'salt', 'type': 'bytes32'}, {'internalType': 'uint256[]', 'name': 'extensions', 'type': 'uint256[]'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'internalType': 'uint256', 'name': 'addedValue', 'type': 'uint256'}], 'name': 'increaseAllowance', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'string', 'name': 'name_', 'type': 'string'}, {'internalType': 'string', 'name': 'symbol_', 'type': 'string'}], 'name': 'initialize', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'l1Address', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'l2Bridge', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'name', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'owner', 'type': 'address'}], 'name': 'nonces', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'owner', 'type': 'address'}, {'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'deadline', 'type': 'uint256'}, {'internalType': 'uint8', 'name': 'v', 'type': 'uint8'}, {'internalType': 'bytes32', 'name': 'r', 'type': 'bytes32'}, {'internalType': 'bytes32', 'name': 's', 'type': 'bytes32'}], 'name': 'permit', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'symbol', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'totalSupply', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'to', 'type': 'address'}, {'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}], 'name': 'transfer', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'from', 'type': 'address'}, {'internalType': 'address', 'name': 'to', 'type': 'address'}, {'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}], 'name': 'transferFrom', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': '_amount', 'type': 'uint256'}], 'name': 'withdraw', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': '_to', 'type': 'address'}, {'internalType': 'uint256', 'name': '_amount', 'type': 'uint256'}], 'name': 'withdrawTo', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'stateMutability': 'payable', 'type': 'receive'}]

NATIVE_ABI = {
    'Starknet':{
        'evm_contract': [{'anonymous': False, 'inputs': [], 'name': 'LogBridgeActivated', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'sender', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}, {'indexed': True, 'internalType': 'uint256', 'name': 'l2Recipient', 'type': 'uint256'}, {'indexed': False, 'internalType': 'uint256', 'name': 'nonce', 'type': 'uint256'}, {'indexed': False, 'internalType': 'uint256', 'name': 'fee', 'type': 'uint256'}], 'name': 'LogDeposit', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'sender', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}, {'indexed': True, 'internalType': 'uint256', 'name': 'l2Recipient', 'type': 'uint256'}, {'indexed': False, 'internalType': 'uint256', 'name': 'nonce', 'type': 'uint256'}], 'name': 'LogDepositCancelRequest', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'sender', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}, {'indexed': True, 'internalType': 'uint256', 'name': 'l2Recipient', 'type': 'uint256'}, {'indexed': False, 'internalType': 'uint256', 'name': 'nonce', 'type': 'uint256'}], 'name': 'LogDepositReclaimed', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'address', 'name': 'acceptedGovernor', 'type': 'address'}], 'name': 'LogNewGovernorAccepted', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'address', 'name': 'nominatedGovernor', 'type': 'address'}], 'name': 'LogNominatedGovernor', 'type': 'event'}, {'anonymous': False, 'inputs': [], 'name': 'LogNominationCancelled', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'address', 'name': 'removedGovernor', 'type': 'address'}], 'name': 'LogRemovedGovernor', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}], 'name': 'LogSetL2TokenBridge', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}], 'name': 'LogSetMaxDeposit', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}], 'name': 'LogSetMaxTotalBalance', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'recipient', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}], 'name': 'LogWithdrawal', 'type': 'event'}, {'inputs': [], 'name': 'acceptGovernance', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'cancelNomination', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'l2Recipient', 'type': 'uint256'}], 'name': 'deposit', 'outputs': [], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'l2Recipient', 'type': 'uint256'}], 'name': 'deposit', 'outputs': [], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'l2Recipient', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'nonce', 'type': 'uint256'}], 'name': 'depositCancelRequest', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'l2Recipient', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'nonce', 'type': 'uint256'}], 'name': 'depositReclaim', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'identify', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'stateMutability': 'pure', 'type': 'function'}, {'inputs': [{'internalType': 'bytes', 'name': 'data', 'type': 'bytes'}], 'name': 'initialize', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'isActive', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'isFrozen', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}], 'name': 'isGovernor', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'maxDeposit', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'maxTotalBalance', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'newGovernor', 'type': 'address'}], 'name': 'nominateNewGovernor', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'governorForRemoval', 'type': 'address'}], 'name': 'removeGovernor', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'l2TokenBridge_', 'type': 'uint256'}], 'name': 'setL2TokenBridge', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'maxDeposit_', 'type': 'uint256'}], 'name': 'setMaxDeposit', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'maxTotalBalance_', 'type': 'uint256'}], 'name': 'setMaxTotalBalance', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}, {'internalType': 'address', 'name': 'recipient', 'type': 'address'}], 'name': 'withdraw', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'amount', 'type': 'uint256'}], 'name': 'withdraw', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}],
        'stark_contract': [{'name': 'Uint256', 'size': 2, 'type': 'struct', 'members': [{'name': 'low', 'type': 'felt', 'offset': 0}, {'name': 'high', 'type': 'felt', 'offset': 1}]}, {'name': 'initialized', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'res', 'type': 'felt'}], 'stateMutability': 'view'}, {'data': [{'name': 'l1_bridge_address', 'type': 'felt'}], 'keys': [], 'name': 'l1_bridge_set', 'type': 'event'}, {'data': [{'name': 'l2_token_address', 'type': 'felt'}], 'keys': [], 'name': 'l2_token_set', 'type': 'event'}, {'data': [{'name': 'l1_recipient', 'type': 'felt'}, {'name': 'amount', 'type': 'Uint256'}, {'name': 'caller_address', 'type': 'felt'}], 'keys': [], 'name': 'withdraw_initiated', 'type': 'event'}, {'data': [{'name': 'account', 'type': 'felt'}, {'name': 'amount', 'type': 'Uint256'}], 'keys': [], 'name': 'deposit_handled', 'type': 'event'}, {'name': 'get_governor', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'res', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'get_l1_bridge', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'res', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'get_l2_token', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'res', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'get_version', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'version', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'get_identity', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'identity', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'initialize', 'type': 'function', 'inputs': [{'name': 'init_vector_len', 'type': 'felt'}, {'name': 'init_vector', 'type': 'felt*'}], 'outputs': []}, {'name': 'set_l1_bridge', 'type': 'function', 'inputs': [{'name': 'l1_bridge_address', 'type': 'felt'}], 'outputs': []}, {'name': 'set_l2_token', 'type': 'function', 'inputs': [{'name': 'l2_token_address', 'type': 'felt'}], 'outputs': []}, {'name': 'initiate_withdraw', 'type': 'function', 'inputs': [{'name': 'l1_recipient', 'type': 'felt'}, {'name': 'amount', 'type': 'Uint256'}], 'outputs': []}, {'name': 'handle_deposit', 'type': 'l1_handler', 'inputs': [{'name': 'from_address', 'type': 'felt'}, {'name': 'account', 'type': 'felt'}, {'name': 'amount_low', 'type': 'felt'}, {'name': 'amount_high', 'type': 'felt'}], 'outputs': []}],
        'braavos': [{'name': 'DeferredRemoveSignerRequest', 'size': 2, 'type': 'struct', 'members': [{'name': 'expire_at', 'type': 'felt', 'offset': 0}, {'name': 'signer_id', 'type': 'felt', 'offset': 1}]}, {'name': 'SignerModel', 'size': 7, 'type': 'struct', 'members': [{'name': 'signer_0', 'type': 'felt', 'offset': 0}, {'name': 'signer_1', 'type': 'felt', 'offset': 1}, {'name': 'signer_2', 'type': 'felt', 'offset': 2}, {'name': 'signer_3', 'type': 'felt', 'offset': 3}, {'name': 'type', 'type': 'felt', 'offset': 4}, {'name': 'reserved_0', 'type': 'felt', 'offset': 5}, {'name': 'reserved_1', 'type': 'felt', 'offset': 6}]}, {'name': 'DeferredMultisigDisableRequest', 'size': 1, 'type': 'struct', 'members': [{'name': 'expire_at', 'type': 'felt', 'offset': 0}]}, {'name': 'IndexedSignerModel', 'size': 8, 'type': 'struct', 'members': [{'name': 'index', 'type': 'felt', 'offset': 0}, {'name': 'signer', 'type': 'SignerModel', 'offset': 1}]}, {'name': 'PendingMultisigTransaction', 'size': 5, 'type': 'struct', 'members': [{'name': 'transaction_hash', 'type': 'felt', 'offset': 0}, {'name': 'expire_at_sec', 'type': 'felt', 'offset': 1}, {'name': 'expire_at_block_num', 'type': 'felt', 'offset': 2}, {'name': 'signer_1_id', 'type': 'felt', 'offset': 3}, {'name': 'is_disable_multisig_transaction', 'type': 'felt', 'offset': 4}]}, {'name': 'AccountCallArray', 'size': 4, 'type': 'struct', 'members': [{'name': 'to', 'type': 'felt', 'offset': 0}, {'name': 'selector', 'type': 'felt', 'offset': 1}, {'name': 'data_offset', 'type': 'felt', 'offset': 2}, {'name': 'data_len', 'type': 'felt', 'offset': 3}]}, {'data': [{'name': 'implementation', 'type': 'felt'}], 'keys': [], 'name': 'Upgraded', 'type': 'event'}, {'data': [{'name': 'request', 'type': 'DeferredRemoveSignerRequest'}], 'keys': [], 'name': 'SignerRemoveRequest', 'type': 'event'}, {'data': [{'name': 'signer_id', 'type': 'felt'}, {'name': 'signer', 'type': 'SignerModel'}], 'keys': [], 'name': 'SignerAdded', 'type': 'event'}, {'data': [{'name': 'signer_id', 'type': 'felt'}], 'keys': [], 'name': 'SignerRemoved', 'type': 'event'}, {'data': [{'name': 'request', 'type': 'DeferredRemoveSignerRequest'}], 'keys': [], 'name': 'SignerRemoveRequestCancelled', 'type': 'event'}, {'data': [{'name': 'public_key', 'type': 'felt'}], 'keys': [], 'name': 'AccountInitialized', 'type': 'event'}, {'data': [{'name': 'request', 'type': 'DeferredMultisigDisableRequest'}], 'keys': [], 'name': 'MultisigDisableRequest', 'type': 'event'}, {'data': [{'name': 'request', 'type': 'DeferredMultisigDisableRequest'}], 'keys': [], 'name': 'MultisigDisableRequestCancelled', 'type': 'event'}, {'data': [{'name': 'num_signers', 'type': 'felt'}], 'keys': [], 'name': 'MultisigSet', 'type': 'event'}, {'data': [], 'keys': [], 'name': 'MultisigDisabled', 'type': 'event'}, {'name': 'supportsInterface', 'type': 'function', 'inputs': [{'name': 'interfaceId', 'type': 'felt'}], 'outputs': [{'name': 'success', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'get_impl_version', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'res', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'initializer', 'type': 'function', 'inputs': [{'name': 'public_key', 'type': 'felt'}], 'outputs': []}, {'name': 'upgrade', 'type': 'function', 'inputs': [{'name': 'new_implementation', 'type': 'felt'}], 'outputs': []}, {'name': 'upgrade_regenesis', 'type': 'function', 'inputs': [{'name': 'new_implementation', 'type': 'felt'}, {'name': 'regenesis_account_id', 'type': 'felt'}], 'outputs': []}, {'name': 'migrate_storage', 'type': 'function', 'inputs': [{'name': 'from_version', 'type': 'felt'}], 'outputs': []}, {'name': 'add_signer', 'type': 'function', 'inputs': [{'name': 'signer', 'type': 'SignerModel'}], 'outputs': [{'name': 'signer_id', 'type': 'felt'}]}, {'name': 'swap_signers', 'type': 'function', 'inputs': [{'name': 'remove_index', 'type': 'felt'}, {'name': 'added_signer', 'type': 'SignerModel'}], 'outputs': [{'name': 'signer_id', 'type': 'felt'}]}, {'name': 'setPublicKey', 'type': 'function', 'inputs': [{'name': 'newPublicKey', 'type': 'felt'}], 'outputs': []}, {'name': 'remove_signer', 'type': 'function', 'inputs': [{'name': 'index', 'type': 'felt'}], 'outputs': []}, {'name': 'remove_signer_with_etd', 'type': 'function', 'inputs': [{'name': 'index', 'type': 'felt'}], 'outputs': []}, {'name': 'cancel_deferred_remove_signer_req', 'type': 'function', 'inputs': [{'name': 'removed_signer_id', 'type': 'felt'}], 'outputs': []}, {'name': 'getPublicKey', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'publicKey', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'get_public_key', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'res', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'get_signers', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'signers_len', 'type': 'felt'}, {'name': 'signers', 'type': 'IndexedSignerModel*'}], 'stateMutability': 'view'}, {'name': 'get_signer', 'type': 'function', 'inputs': [{'name': 'index', 'type': 'felt'}], 'outputs': [{'name': 'signer', 'type': 'SignerModel'}], 'stateMutability': 'view'}, {'name': 'get_deferred_remove_signer_req', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'deferred_request', 'type': 'DeferredRemoveSignerRequest'}], 'stateMutability': 'view'}, {'name': 'get_execution_time_delay', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'etd_sec', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'is_valid_signature', 'type': 'function', 'inputs': [{'name': 'hash', 'type': 'felt'}, {'name': 'signature_len', 'type': 'felt'}, {'name': 'signature', 'type': 'felt*'}], 'outputs': [{'name': 'is_valid', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'isValidSignature', 'type': 'function', 'inputs': [{'name': 'hash', 'type': 'felt'}, {'name': 'signature_len', 'type': 'felt'}, {'name': 'signature', 'type': 'felt*'}], 'outputs': [{'name': 'isValid', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'get_multisig', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'multisig_num_signers', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'set_multisig', 'type': 'function', 'inputs': [{'name': 'num_signers', 'type': 'felt'}], 'outputs': []}, {'name': 'get_pending_multisig_transaction', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'pending_multisig_transaction', 'type': 'PendingMultisigTransaction'}], 'stateMutability': 'view'}, {'name': 'sign_pending_multisig_transaction', 'type': 'function', 'inputs': [{'name': 'pending_calldata_len', 'type': 'felt'}, {'name': 'pending_calldata', 'type': 'felt*'}, {'name': 'pending_nonce', 'type': 'felt'}, {'name': 'pending_max_fee', 'type': 'felt'}, {'name': 'pending_transaction_version', 'type': 'felt'}], 'outputs': [{'name': 'response_len', 'type': 'felt'}, {'name': 'response', 'type': 'felt*'}]}, {'name': 'disable_multisig', 'type': 'function', 'inputs': [], 'outputs': []}, {'name': 'disable_multisig_with_etd', 'type': 'function', 'inputs': [], 'outputs': []}, {'name': 'get_deferred_disable_multisig_req', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'deferred_request', 'type': 'DeferredMultisigDisableRequest'}], 'stateMutability': 'view'}, {'name': 'cancel_deferred_disable_multisig_req', 'type': 'function', 'inputs': [], 'outputs': []}, {'name': '__validate__', 'type': 'function', 'inputs': [{'name': 'call_array_len', 'type': 'felt'}, {'name': 'call_array', 'type': 'AccountCallArray*'}, {'name': 'calldata_len', 'type': 'felt'}, {'name': 'calldata', 'type': 'felt*'}], 'outputs': []}, {'name': '__validate_deploy__', 'type': 'function', 'inputs': [{'name': 'class_hash', 'type': 'felt'}, {'name': 'contract_address_salt', 'type': 'felt'}, {'name': 'implementation_address', 'type': 'felt'}, {'name': 'initializer_selector', 'type': 'felt'}, {'name': 'calldata_len', 'type': 'felt'}, {'name': 'calldata', 'type': 'felt*'}], 'outputs': []}, {'name': '__validate_declare__', 'type': 'function', 'inputs': [{'name': 'class_hash', 'type': 'felt'}], 'outputs': []}, {'name': '__execute__', 'type': 'function', 'inputs': [{'name': 'call_array_len', 'type': 'felt'}, {'name': 'call_array', 'type': 'AccountCallArray*'}, {'name': 'calldata_len', 'type': 'felt'}, {'name': 'calldata', 'type': 'felt*'}], 'outputs': [{'name': 'response_len', 'type': 'felt'}, {'name': 'response', 'type': 'felt*'}]}, {'name': 'get_implementation', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'implementation', 'type': 'felt'}], 'stateMutability': 'view'}],
        'argent': [{'name': 'CallArray', 'size': 4, 'type': 'struct', 'members': [{'name': 'to', 'type': 'felt', 'offset': 0}, {'name': 'selector', 'type': 'felt', 'offset': 1}, {'name': 'data_offset', 'type': 'felt', 'offset': 2}, {'name': 'data_len', 'type': 'felt', 'offset': 3}]}, {'data': [{'name': 'new_signer', 'type': 'felt'}], 'keys': [], 'name': 'signer_changed', 'type': 'event'}, {'data': [{'name': 'new_guardian', 'type': 'felt'}], 'keys': [], 'name': 'guardian_changed', 'type': 'event'}, {'data': [{'name': 'new_guardian', 'type': 'felt'}], 'keys': [], 'name': 'guardian_backup_changed', 'type': 'event'}, {'data': [{'name': 'active_at', 'type': 'felt'}], 'keys': [], 'name': 'escape_guardian_triggered', 'type': 'event'}, {'data': [{'name': 'active_at', 'type': 'felt'}], 'keys': [], 'name': 'escape_signer_triggered', 'type': 'event'}, {'data': [], 'keys': [], 'name': 'escape_canceled', 'type': 'event'}, {'data': [{'name': 'new_guardian', 'type': 'felt'}], 'keys': [], 'name': 'guardian_escaped', 'type': 'event'}, {'data': [{'name': 'new_signer', 'type': 'felt'}], 'keys': [], 'name': 'signer_escaped', 'type': 'event'}, {'data': [{'name': 'new_implementation', 'type': 'felt'}], 'keys': [], 'name': 'account_upgraded', 'type': 'event'}, {'data': [{'name': 'account', 'type': 'felt'}, {'name': 'key', 'type': 'felt'}, {'name': 'guardian', 'type': 'felt'}], 'keys': [], 'name': 'account_created', 'type': 'event'}, {'data': [{'name': 'hash', 'type': 'felt'}, {'name': 'response_len', 'type': 'felt'}, {'name': 'response', 'type': 'felt*'}], 'keys': [], 'name': 'transaction_executed', 'type': 'event'}, {'name': '__validate__', 'type': 'function', 'inputs': [{'name': 'call_array_len', 'type': 'felt'}, {'name': 'call_array', 'type': 'CallArray*'}, {'name': 'calldata_len', 'type': 'felt'}, {'name': 'calldata', 'type': 'felt*'}], 'outputs': []}, {'name': '__execute__', 'type': 'function', 'inputs': [{'name': 'call_array_len', 'type': 'felt'}, {'name': 'call_array', 'type': 'CallArray*'}, {'name': 'calldata_len', 'type': 'felt'}, {'name': 'calldata', 'type': 'felt*'}], 'outputs': [{'name': 'retdata_size', 'type': 'felt'}, {'name': 'retdata', 'type': 'felt*'}]}, {'name': '__validate_declare__', 'type': 'function', 'inputs': [{'name': 'class_hash', 'type': 'felt'}], 'outputs': []}, {'name': '__validate_deploy__', 'type': 'function', 'inputs': [{'name': 'selector', 'type': 'felt'}, {'name': 'calldata_size', 'type': 'felt'}, {'name': 'calldata', 'type': 'felt*'}], 'outputs': []}, {'name': 'isValidSignature', 'type': 'function', 'inputs': [{'name': 'hash', 'type': 'felt'}, {'name': 'sig_len', 'type': 'felt'}, {'name': 'sig', 'type': 'felt*'}], 'outputs': [{'name': 'isValid', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'supportsInterface', 'type': 'function', 'inputs': [{'name': 'interfaceId', 'type': 'felt'}], 'outputs': [{'name': 'success', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'initialize', 'type': 'function', 'inputs': [{'name': 'signer', 'type': 'felt'}, {'name': 'guardian', 'type': 'felt'}], 'outputs': []}, {'name': 'upgrade', 'type': 'function', 'inputs': [{'name': 'implementation', 'type': 'felt'}, {'name': 'calldata_len', 'type': 'felt'}, {'name': 'calldata', 'type': 'felt*'}], 'outputs': [{'name': 'retdata_len', 'type': 'felt'}, {'name': 'retdata', 'type': 'felt*'}]}, {'name': 'execute_after_upgrade', 'type': 'function', 'inputs': [{'name': 'call_array_len', 'type': 'felt'}, {'name': 'call_array', 'type': 'CallArray*'}, {'name': 'calldata_len', 'type': 'felt'}, {'name': 'calldata', 'type': 'felt*'}], 'outputs': [{'name': 'retdata_len', 'type': 'felt'}, {'name': 'retdata', 'type': 'felt*'}]}, {'name': 'changeSigner', 'type': 'function', 'inputs': [{'name': 'newSigner', 'type': 'felt'}], 'outputs': []}, {'name': 'changeGuardian', 'type': 'function', 'inputs': [{'name': 'newGuardian', 'type': 'felt'}], 'outputs': []}, {'name': 'changeGuardianBackup', 'type': 'function', 'inputs': [{'name': 'newGuardian', 'type': 'felt'}], 'outputs': []}, {'name': 'triggerEscapeGuardian', 'type': 'function', 'inputs': [], 'outputs': []}, {'name': 'triggerEscapeSigner', 'type': 'function', 'inputs': [], 'outputs': []}, {'name': 'cancelEscape', 'type': 'function', 'inputs': [], 'outputs': []}, {'name': 'escapeGuardian', 'type': 'function', 'inputs': [{'name': 'newGuardian', 'type': 'felt'}], 'outputs': []}, {'name': 'escapeSigner', 'type': 'function', 'inputs': [{'name': 'newSigner', 'type': 'felt'}], 'outputs': []}, {'name': 'getSigner', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'signer', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'getGuardian', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'guardian', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'getGuardianBackup', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'guardianBackup', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'getEscape', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'activeAt', 'type': 'felt'}, {'name': 'type', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'getVersion', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'version', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'getName', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'name', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'is_valid_signature', 'type': 'function', 'inputs': [{'name': 'hash', 'type': 'felt'}, {'name': 'sig_len', 'type': 'felt'}, {'name': 'sig', 'type': 'felt*'}], 'outputs': [{'name': 'is_valid', 'type': 'felt'}], 'stateMutability': 'view'}, {'name': 'get_implementation', 'type': 'function', 'inputs': [], 'outputs': [{'name': 'implementation', 'type': 'felt'}], 'stateMutability': 'view'}],
    }
}

ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'

ETH_MASK = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

NATIVE_CONTRACTS_PER_CHAIN = {
    'Starknet': {
        "evm_contract"       : "0xae0Ee0A63A2cE6BaeEFFE56e7714FB4EFE48D419",
        "stark_contract"     :  0x073314940630fd6dcda0d772d4c972c4e0a9946bef9dabf4ef84eda8ef542b82,
    }
}

TOKENS_PER_CHAIN = {
    'Ethereum': {
        'USDC'              : '0xdAC17F958D2ee523a2206206994597C13D831ec7',
        'USDT'              : '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    },
    "Avalanche": {
        'USDC'              : '0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E',
        'USDT'              : '0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7',
    },
    "Arbitrum":{
        "ETH"               : "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        "WETH"              : "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        'USDC'              : "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
        'USDT'              : "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
        'USDC.e'            : "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",
        'DAI'               : "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
    },
    'Arbitrum Nova':{
        "ETH"               : "0x722E8BdD2ce80A4422E880164f2079488e115365",
        "WETH"              : "0x722E8BdD2ce80A4422E880164f2079488e115365",
        "DAI"               : "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1"
    },
    'Zora':{
        "ETH"               : "0x4200000000000000000000000000000000000006",
        "WETH"              : "0x4200000000000000000000000000000000000006"
    },
    "Optimism":{
        "ETH"               : "0x4200000000000000000000000000000000000006",
        "WETH"              : "0x4200000000000000000000000000000000000006",
        "USDC"              : "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85",
        "USDT"              : "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58",
        "USDC.e"            : "0x7F5c764cBc14f9669B88837ca1490cCa17c31607",
        "DAI"               : "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1"
    },
    "Polygon":{
        'MATIC'             : "0x0000000000000000000000000000000000001010",
        'WETH'              : "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        'USDT'              : "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
        'USDC'              : "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
        'USDC.e'            : "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
    },
    "zkSync": {
        "ETH"               : "0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91",
        "WETH"              : "0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91",
        "USDC"              : "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4",
        "USDT"              : "0x493257fD37EDB34451f62EDf8D2a0C418852bA4C",
        "BUSD"              : "0x2039bb4116B4EFc145Ec4f0e2eA75012D6C0f181"
    },
    "Starknet": {
        "ETH"               : 0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7,
        "USDC"              : 0x053c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8,
        "USDT"              : 0x068f5c6a61780768455de69077e07e89787839bf8166decfbf92b645209c0fb8,
        "DAI"               : 0x00da114221cb83fa859dbdb4c44beeaa0bb37c7537ad5ae66fe5e0efd20e6eb3,
    },
    "Base":{
        "ETH"               : "0x4200000000000000000000000000000000000006",
        "WETH"              : "0x4200000000000000000000000000000000000006",
        "USDC"              : "0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA",
    },
    "Linea":{
        "ETH"               : "0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f",
        "WETH"              : "0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f",
        #"USDT"              : "0xA219439258ca9da29E9Cc4cE5596924745e12B93",
        "USDC"              : "0x176211869cA2b568f2A7D4EE941E073a821EE1ff",
    },
    "Scroll":{
        "ETH"               : "0x5300000000000000000000000000000000000004",
        "WETH"              : "0x5300000000000000000000000000000000000004",
        "USDT"              : "0xf55BEC9cafDbE8730f096Aa55dad6D22d44099Df",
        "USDC"              : "0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4",
    },
    "BNB Chain":{
        "USDT"              : "0x55d398326f99059fF775485246999027B3197955",
        "USDC"              : "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
    },
    "Manta":{
        "ETH"               : "0x0Dc808adcE2099A9F62AA87D9670745AbA741746",
        "WETH"              : "0x0Dc808adcE2099A9F62AA87D9670745AbA741746",
        "USDT"              : "0xf417F5A458eC102B90352F697D6e2Ac3A3d2851f",
        "USDC"              : "0xb73603C5d87fA094B7314C74ACE2e64D165016fb",
    }
}

AVNU_CONTRACT = {
    'router'                : 0x04270219d365d6b017231b52e92b3fb5d7c8378b05e9abc97724537a80e93b0f
}

CARMINE_CONTRACT = {
    'landing'               : 0x076dbabc4293db346b0a56b29b6ea9fe18e93742c73f12348c8747ecfc1050aa
}


SPACESHARD_CONTRACT = {
    'core'                  : 0x06e02b62e101b44382d030d7aee5528bf65eed13d3b2d5da3dfa883a2e1ce5f7
}


STARKSTARS_COUNTACTS = {
    1                       : 0x04d70758d392e0563a8a0076d4b72847048dea7d65199c50eabc8e855ca62931,
    2                       : 0x02ac5be4b280f6625a56b944bab9d985fbbc9f180ff4b08b854b63d284b7f6ae,
    3                       : 0x05f650c37f8a15e33f01b3c28365637ca72a536014c4b8f84271c20a4c24aef8,
    4                       : 0x027c8cb6bf861df8b86ebda8656430aeec9c1c2c66e9f99d3c8587df5fcb1c9c,
    5                       : 0x05e69ae81aed84dfadb4af03a67ce702e353db7f7f87ad833cf08df36e427704,
    6                       : 0x06b1e710f97e0d4701123c256a6f4cce4ffdc2bf6f439b42f48d08585feab123,
    7                       : 0x062b37f6ced8e742ecd4baa51321e0c39ab089183a1ca0b24138e1fb0f5083a8,
    8                       : 0x0656c27654b2b3c4ae3e8f5f6bc2a4863a79fb74cb7b2999af9dde2ad1fe3cb5,
    9                       : 0x0265f815955a1595e6859f3ad80533f15b2b57311d25fed6f01e4c530c1f1b0f,
    10                      : 0x02c69468dd31a6837bc4a10357bc940f41f6d0acebe74376c940195915cede1d,
    11                      : 0x0040cb48ec6f61e1bbc5b62ee2f7a7df8151712394248c90db4f12f7a61ce993,
    12                      : 0x04aa60106c215809a9dfc2ac2d64aa166f1185e9dc7212497a837f7d60bfb1c3,
    13                      : 0x0002ff063073208cd8b867c727be3a5f46c54d31ae1c1fbf7506ffaca673990f,
    14                      : 0x07bc362ffdbd67ff80b49e95f0b9996ad89f9f6ea9186d209ece577df429e69b,
    15                      : 0x0267217f031a1d794446943ba45175153d18202b3db246db6b15b0c772f9ec09,
    16                      : 0x0021461d8b7593ef6d39a83229750d61a23b7f45b91baafb5ad1b2da6abf13c0,
    17                      : 0x04c7999fb6eeb958240abdecdddc2331f35b5f99f1e60e29ef0e4e26f23e182b,
    18                      : 0x050e02814bd1900efd33148dbed847e7fe42a2a2de6dd444366ead20cf8dedc5,
    19                      : 0x03883b7148c475f170c4b1a21e37b15b9261e86f9c203098ff1c3b7f8cf72f73,
    20                      : 0x0394034029c6c0773397a2c79eb9b7df8f080613bfec83d93c3cd5e7c0b993ce
}


PROTOSS_CONTRACT = {
    "router"                : 0x07a0922657e550ba1ef76531454cb6d203d4d168153a0f05671492982c2f7741
}


SITHSWAP_CONTRACT = {
    'router'                : 0x28c858a586fa12123a1ccb337a0a3b369281f91ea00544d0c086524b759f627
}

ZKLEND_CONTRACTS = {
    "landing"               : 0x04c0a5193d58f74fbace4b74dcf65481e734ed1714121bdc571da345540efa05,
    "ETH"                   : 0x01b5bd713e72fdc5d63ffd83762f81297f6175a5e0a4771cdadbc1dd5fe72cb1,
    "USDC"                  : 0x047ad51726d891f972e74e4ad858a261b43869f7126ce7436ee0b2529a98f486,
    "USDT"                  : 0x00811d8da5dc8a2206ea7fd0b28627c2d77280a515126e62baa4d78e22714c4a,
    "DAI"                   : 0x062fa7afe1ca2992f8d8015385a279f49fad36299754fb1e9866f4f052289376
}

NOSTRA_CONTRACTS = {
    "ETH"                   : 0x07170f54dd61ae85377f75131359e3f4a12677589bb7ec5d61f362915a5c0982,
    "USDC"                  : 0x06eda767a143da12f70947192cd13ee0ccc077829002412570a88cd6539c1d85,
    "USDT"                  : 0x0453c4c996f1047d9370f824d68145bd5e7ce12d00437140ad02181e1d11dc83,
    "DAI"                   : 0x04f18ffc850cdfa223a530d7246d3c6fc12a5969e0aa5d4a88f470f5fe6c46e9
}

STARKNET_ID_CONTRACT = {
    'register'              : 0x05dbdedc203e92749e2e746e2d40a768d966bd243df04a6b712e222bc040a9af
}

DMAIL_CONTRACT = {
    'Starknet': {
        'core'              : 0x0454f0bd015e730e5adbb4f080b075fdbf55654ff41ee336203aa2e1ac4d4309
    }
}

MYSWAP_CONTRACT = {
    'router'                : 0x010884171baf1914edc28d7afb619b40a4051cfae78a094a55d230f19e944a28
}

TENKSWAP_CONTRACT = {
    'router'                : 0x07a6f98c03379b9513ca84cca1373ff452a7462a3b61598f0af5bb27ad7f76d1
}

JEDISWAP_CONTRACT = {
    'router'                : 0x041fd22b238fa21cfcf5dd45a8548974d8263b3a531a60388411c5e230f97023
}

BRAAVOS_PROXY_CLASS_HASH = 0x03131fa018d520a037686ce3efddeab8f28895662f019ca3ca18a626650f7d1e
BRAAVOS_IMPLEMENTATION_CLASS_HASH = 0x5aa23d5bb71ddaa783da7ea79d405315bafa7cf0387a74f4593578c3e9e6570
BRAAVOS_IMPLEMENTATION_CLASS_HASH_NEW = 0x05dec330eebf36c8672b60db4a718d44762d3ae6d1333e553197acb47ee5a062

ARGENT_PROXY_CLASS_HASH = 0x025EC026985A3BF9D0CC1FE17326B245DFDC3FF89B8FDE106542A3EA56C5A918
ARGENT_IMPLEMENTATION_CLASS_HASH = 0x033434AD846CDD5F23EB73FF09FE6FDDD568284A0FB7D1BE20EE482F044DABE2
ARGENT_IMPLEMENTATION_CLASS_HASH_NEW = 0x01a736d6ed154502257f02b1ccdf4d9d1089f80811cd6acad48e6b6a9d1f2003

ORBITER_CONTRACTS = {
    "evm_contracts"         : {
        'zkSync'            :'0xBF3922a0cEBbcD718e715e83d9187cC4BbA23f11',
        'Zora'              :'0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
        'Arbitrum'          :'0xD9D74a29307cc6Fc8BF424ee4217f1A587FBc8Dc',
        'Arbitrum Nova'     :'0xD9D74a29307cc6Fc8BF424ee4217f1A587FBc8Dc',
        'Base'              :'0xD9D74a29307cc6Fc8BF424ee4217f1A587FBc8Dc',
        'Linea'             :'0xD9D74a29307cc6Fc8BF424ee4217f1A587FBc8Dc',
        'Manta'             :'0xD9D74a29307cc6Fc8BF424ee4217f1A587FBc8Dc',
        'Polygon'           :'0xD9D74a29307cc6Fc8BF424ee4217f1A587FBc8Dc',
        'Polygon ZKEVM'     :'0xD9D74a29307cc6Fc8BF424ee4217f1A587FBc8Dc',
    },
    "stark_contract"        : 0x173f81c529191726c6e7287e24626fe24760ac44dae2a1f7e02080230f8458b
}

LAYERSWAP_CHAIN_NAME = {
    1                       : 'ARBITRUM_MAINNET',
    2                       : 'ARBITRUMNOVA_MAINNET',
    3                       : 'BASE_MAINNET',
    4                       : 'LINEA_MAINNET',
    5                       : 'MANTA_MAINNET',
    6                       : 'POLYGON_MAINNET',
    7                       : 'OPTIMISM_MAINNET',
    8                       : 'SCROLL_MAINNET',
    9                       : 'STARKNET_MAINNET',
    10                      : 'POLYGONZK_MAINNET',
    11                      : 'ZKSYNCERA_MAINNET',
    12                      : 'ZORA_MAINNET',
    13                      : 'ETHEREUM_MAINNET',
    14                      : 'AVAX_MAINNET',
    15                      : 'BSC_MAINNET',
    28                      : 'OPBNB_MAINNET',
    29                      : 'MANTLE_MAINNET',
}

ORBITER_CHAINS_INFO = {
    1:  {'name': 'Arbitrum',       'chainId': 42161,        'id': 2},
    2:  {'name': 'Arbitrum Nova',  'chainId': 42170,        'id': 16},
    3:  {'name': 'Base',           'chainId': 8453,         'id': 21},
    4:  {'name': 'Linea',          'chainId': 59144,        'id': 23},
    5:  {'name': 'Manta',          'chainId': 169,          'id': 31},
    6:  {'name': 'Polygon',        'chainId': 137,          'id': 6},
    7:  {'name': 'Optimism',       'chainId': 10,           'id': 7},
    8:  {'name': 'Scroll',         'chainId': 534352,       'id': 19},
    9:  {'name': 'Starknet',       'chainId': 'SN_MAIN',    'id': 4},
    10: {'name': 'Polygon zkEVM',  'chainId': 1101,         'id': 17},
    11: {'name': 'zkSync Era',     'chainId': 324,          'id': 14},
    12: {'name': 'Zora',           'chainId': 7777777,      'id': 30},
    13: {'name': 'Ethereum',       'chainId': 1,            'id': 1},
    14: {'name': 'BNB Chain',      'chainId': 56,           'id': 15},
    26: {'name': 'Metis',          'chainId': 1088,         'id': 10},
    28: {'name': 'OpBNB',          'chainId': 204,          'id': 25},
    29: {'name': 'Mantle',         'chainId': 5000,         'id': 24},
    45: {'name': 'ZKFair',         'chainId': 42766,        'id': 38}
}

CHAIN_IDS = {
    1:  42161,
    2:  42170,
    3:  8453,
    4:  59144,
    5:  169,
    6:  137,
    7:  10,
    8:  534352,
    9:  'SN_MAIN',
    10: 1101,
    11: 324,
    12: 7777777,
    13: 1,
    14: 43114,
    15: 56,
}

RHINO_CHAIN_INFO = {
    1: 'ARBITRUM',
    2: 'ARBITRUMNOVA',
    3: 'BASE',
    4: 'LINEA',
    5: 'MANTA',
    6: 'MATIC_POS',
    7: 'OPTIMISM',
    8: 'SCROLL',
    9: 'STARKNET',
    10: 'ZKEVM',
    11: 'ZKSYNC',
}

CHAIN_NAME_FROM_ID = {
    42161: 'Arbitrum',
    42170: 'Arbitrum Nova',
    8453: 'Base',
    59144: 'Linea',
    169: 'Manta',
    137: 'Polygon',
    10: 'Optimism',
    534352: 'Scroll',
    'SN_MAIN': 'Starknet',
    1101: 'Polygon ZKEVM',
    324: 'zkSync',
    7777777: 'Zora',
    1: 'Ethereum',
}

OKX_NETWORKS_NAME = {
    1                       : 'ETH-ERC20',
    2                       : 'ETH-Arbitrum One',
    3                       : 'ETH-Optimism',
    4                       : 'ETH-zkSync Era',
    5                       : 'ETH-Linea',
    6                       : 'ETH-Base',
    7                       : 'AVAX-Avalanche C-Chain',
    8                       : 'BNB-BSC',
    # 9                    : 'BNB-OPBNB',
    10                      : 'CELO-CELO',
    11                      : 'GLMR-Moonbeam',
    12                      : 'MOVR-Moonriver',
    13                      : 'METIS-Metis',
    14                      : 'CORE-CORE',
    15                      : 'CFX-CFX_EVM',
    16                      : 'KLAY-Klaytn',
    17                      : 'FTM-Fantom',
    18                      : 'MATIC-Polygon',
    19                      : 'USDT-Arbitrum One',
    20                      : 'USDT-Avalanche',
    21                      : 'USDT-Optimism',
    22                      : 'USDT-Polygon',
    23                      : 'USDT-BSC',
    24                      : 'USDT-ERC20',
    25                      : 'USDC-Arbitrum One',
    26                      : 'USDC-Avalanche C-Chain',
    27                      : 'USDC-Optimism',
    28                      : 'USDC-Polygon',
    29                      : 'USDC-Optimism (Bridged)',
    30                      : 'USDC-Polygon (Bridged)',
    31                      : 'USDC-BSC',
    32                      : 'USDC-ERC20',
}

BINGX_NETWORKS_NAME = {
    1                       : "ETH-ERC20",
    2                       : "ETH-ARBITRUM",
    3                       : "ETH-OPTIMISM",
    4                       : "ETH-ZKSYNCERA",
    5                       : "ETH-LINEA",
    6                       : "ETH-BASE",
    7                       : 'AVAX-AVAX-C',
    8                       : 'BNB-BEP20',
    # 9                      : 'BNB-OPBNB',
    # 10                      : 'CELO-CELO',
    # 11                    : 'GLMR-Moonbeam',
    # 12                    : 'MOVR-Moonriver',
    13                      : 'METIS-METIS',
    # 14                    : 'CORE-CORE',
    15                      : 'CFX-CFX',
    16                      : 'KLAY-KLAYTN',
    17                      : 'FTM-FANTOM',
    18                      : 'MATIC-POLYGON',
    19                      : 'USDT-ARBITRUM',
    # 20                    : 'USDT-Avalanche',
    21                      : 'USDT-OPTIMISM',
    22                      : 'USDT-POLYGON',
    23                      : 'USDT-BEP20',
    24                      : 'USDT-ERC20',
    25                      : 'USDC-Arbitrum One (Circle)',
    26                      : 'USDC-AVAX-C',
    27                      : 'USDC-Optimism (Circle)',
    28                      : 'USDC-Polygon (Circle)',
    29                      : 'USDC-Optimism (Bridged)',
    30                      : 'USDC-Polygon (Bridged)',
    31                      : 'USDC-BEP20',
    32                      : 'USDC-ERC20',
}

BINANCE_NETWORKS_NAME = {
    1                       : "ETH-ETH",
    2                       : "ETH-ARBITRUM",
    3                       : "ETH-OPTIMISM",
    4                       : "ETH-ZKSYNCERA",
    # 5                     : "ETH-LINEA",
    6                       : "ETH-BASE",
    7                       : 'AVAX-AVAXC',
    8                       : 'BNB-BSC',
    9                      : 'BNB-OPBNB',
    10                      : 'CELO-CELO',
    11                      : 'GLMR-Moonbeam',
    12                      : 'MOVR-Moonriver',
    # 13                    : 'METIS-METIS',
    # 14                    : 'CORE-CORE',
    15                      : 'CFX-CFX',
    16                      : 'KLAY-KLAYTN',
    17                      : 'FTM-FANTOM',
    18                      : 'MATIC-MATIC',
    19                      : 'USDT-ARBITRUM',
    20                      : 'USDT-AVAXC',
    21                      : 'USDT-OPTIMISM',
    22                      : 'USDT-MATIC',
    23                      : 'USDT-BSC',
    24                      : 'USDT-ETH',
    25                      : 'USDC-ARBITRUM',
    26                      : 'USDC-AVAXC',
    27                      : 'USDC-OPTIMISM',
    28                      : 'USDC-MATIC',
    # 29                    : 'USDC-Optimism (Bridged)',
    # 30                    : 'USDC-Polygon (Bridged)',
    31                      : 'USDC-BSC',
    32                      : 'USDC-ETH',
}

CEX_WRAPPED_ID = {
     1                          : 13,
     2                          : 1,
     3                          : 7,
     4                          : 11,
     5                          : 4,
     6                          : 3,
     7                          : 14,
     8                          : 15,
     9                          : 28,
     10                         : 19,
     11                         : 16,
     12                         : 30,
     13                         : 26,
     14                         : 21,
     15                         : 23,
     16                         : 31,
     17                         : 33,
     18                         : 6,
     19                         : 1,
     20                         : 14,
     21                         : 7,
     22                         : 6,
     23                         : 15,
     24                         : 13,
     25                         : 1,
     26                         : 14,
     27                         : 7,
     28                         : 6,
     29                         : 7,
     30                         : 6,
     31                         : 15,
     32                         : 1,
}

COINGECKO_TOKEN_API_NAMES = {
     'ETH': 'ethereum',
     'ASTR': 'astar',
     'AVAX': 'avalanche-2',
     'BNB': 'binancecoin',
     'CANTO': 'canto',
     'CELO': 'celo',
     'CFX': 'conflux-token',
     'COREDAO': 'coredaoorg',
     'JEWEL': 'defi-kingdoms',
     'FTM': 'fantom',
     'FUSE': 'fuse-network-token',
     'GETH': 'goerli-eth',
     'xDAI': 'xdai',
     'ONE': 'harmony',
     'ZEN': 'zencash',
     'KAVA': 'kava',
     'KLAY': 'klay-token',
     'AGLD': 'adventure-gold',
     'MNT': 'mantle',
     'MTR': 'meter-stable',
     'METIS': 'metis-token',
     'GLMR': 'moonbeam',
     'MOVR': 'moonriver',
     'OKT': 'oec-token',
     'MATIC': 'matic-network',
     'SMR': 'shimmer',
     'TLOS': 'telos',
     'TOMOE': 'tomoe',
     'TENET': 'tenet-1b000f7b-59cb-4e06-89ce-d62b32d362b9',
     'XPLA': 'xpla',
     'BEAM': 'beam-2',
     'INJ': 'injective-protocol',
     'ETH ': 'ethereum',
}

HELP_SOFTWARE = True  # True or False | True = You support me 1% amount of transactions on aggregator`s

CHAIN_NAME = {
    0: 'OMNI-CHAIN',
    1: 'Arbitrum',
    2: 'Arbitrum Nova',
    3: 'Base',
    4: 'Linea',
    5: 'Manta',
    6: 'Polygon',
    7: 'Optimism',
    8: 'Scroll',
    9: 'Starknet',
    10: 'Polygon ZKEVM',
    11: 'zkSync Era',
    12: 'Zora',
    13: 'Etherium',
    14: 'Avalanch',
    15: 'BNB Chain',
    16: 'Moonbeam',
    17: 'Harmony ONE',
    18: 'Telos',
    19: 'Celo',
    20: 'Gnosis',
    21: 'CoreDAO',
    22: 'TomoChai',
    23: 'Conflux',
    24: 'Orderly',
    25: 'Horizen',
    26: 'Metis',
    27: 'Astar',
    28: 'OpBNB',
    29: 'Mantle',
    30: 'Moonriver',
    31: 'Klaytn',
    32: 'Kava',
    33: 'Fantom',
    34: 'Aurora',
    35: 'Canto',
    36: 'DFK',
    37: 'Fuse',
    38: 'Goerli',
    39: 'Meter',
    40: 'OKX-Chain',
    41: 'Shimmer',
    42: 'Tenet',
    43: 'XPLA',
    44: 'LootChain',
    45: 'ZKFair',
    46: 'Beam',
    47: 'inEVM',
}


TITLE = """
 █████╗ ████████╗████████╗ █████╗  ██████╗██╗  ██╗    ███╗   ███╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗███████╗
██╔══██╗╚══██╔══╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝    ████╗ ████║██╔══██╗██╔════╝██║  ██║██║████╗  ██║██╔════╝
███████║   ██║      ██║   ███████║██║     █████╔╝     ██╔████╔██║███████║██║     ███████║██║██╔██╗ ██║█████╗  
██╔══██║   ██║      ██║   ██╔══██║██║     ██╔═██╗     ██║╚██╔╝██║██╔══██║██║     ██╔══██║██║██║╚██╗██║██╔══╝  
██║  ██║   ██║      ██║   ██║  ██║╚██████╗██║  ██╗    ██║ ╚═╝ ██║██║  ██║╚██████╗██║  ██║██║██║ ╚████║███████╗
╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝
"""

ACCOUNT_NAMES, PRIVATE_KEYS_EVM, PRIVATE_KEYS, PROXIES, CEX_WALLETS = get_accounts_data()

ETH_PRICE = asyncio.run(get_eth_price())
