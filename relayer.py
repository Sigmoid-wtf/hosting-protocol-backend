import json
import os
import shutil
import subprocess
import uuid

from web3 import Web3


SHIFT = 13
PRIVATE_KEY = 'XXXX'

OLAS_CONTRACT_ADDRESS = '0xcE11e14225575945b8E6Dc0D4F2dD4C570f79d9f'
OLAS_CONTRACT_ABI = '[{"constant":true,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"result","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_bridgeContract","type":"address"}],"name":"setBridgeContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_sender","type":"address"},{"name":"_recipient","type":"address"},{"name":"_amount","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"name":"result","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"},{"name":"_data","type":"bytes"}],"name":"transferAndCall","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_value","type":"uint256"}],"name":"burn","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"version","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_subtractedValue","type":"uint256"}],"name":"decreaseApproval","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_token","type":"address"},{"name":"_to","type":"address"}],"name":"claimTokens","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"isBridge","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"finishMinting","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"nonces","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTokenInterfacesVersion","outputs":[{"name":"major","type":"uint64"},{"name":"minor","type":"uint64"},{"name":"patch","type":"uint64"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_holder","type":"address"},{"name":"_spender","type":"address"},{"name":"_nonce","type":"uint256"},{"name":"_expiry","type":"uint256"},{"name":"_allowed","type":"bool"},{"name":"_v","type":"uint8"},{"name":"_r","type":"bytes32"},{"name":"_s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"push","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"move","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH_LEGACY","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"bridgeContract","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_holder","type":"address"},{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"},{"name":"_deadline","type":"uint256"},{"name":"_v","type":"uint8"},{"name":"_r","type":"bytes32"},{"name":"_s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_addedValue","type":"uint256"}],"name":"increaseApproval","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_amount","type":"uint256"}],"name":"pull","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"expirations","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint8"},{"name":"_chainId","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"amount","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[],"name":"MintFinished","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"previousOwner","type":"address"}],"name":"OwnershipRenounced","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"previousOwner","type":"address"},{"indexed":true,"name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"burner","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"},{"indexed":false,"name":"data","type":"bytes"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]'

OLAS_MANAGER_CONTRACT_ADDRESS = '0xeB6c1B13C221D6A2de5D224712B124458272f536'
OLAS_MANAGER_CONTRACT_ABI = '[{"inputs":[{"internalType":"address","name":"_olasToken","type":"address"},{"internalType":"address","name":"_admin","type":"address"},{"internalType":"address","name":"_relayer","type":"address"},{"internalType":"address","name":"_treasury","type":"address"},{"internalType":"address","name":"_emergencyTreasury","type":"address"},{"internalType":"uint256","name":"_maxThreshold","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"target","type":"address"}],"name":"AddressEmptyCode","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"AddressInsufficientBalance","type":"error"},{"inputs":[],"name":"AllowanceNotSet","type":"error"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"allowance","type":"uint256"},{"internalType":"uint256","name":"needed","type":"uint256"}],"name":"ERC20InsufficientAllowance","type":"error"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"uint256","name":"balance","type":"uint256"},{"internalType":"uint256","name":"needed","type":"uint256"}],"name":"ERC20InsufficientBalance","type":"error"},{"inputs":[{"internalType":"address","name":"approver","type":"address"}],"name":"ERC20InvalidApprover","type":"error"},{"inputs":[{"internalType":"address","name":"receiver","type":"address"}],"name":"ERC20InvalidReceiver","type":"error"},{"inputs":[{"internalType":"address","name":"sender","type":"address"}],"name":"ERC20InvalidSender","type":"error"},{"inputs":[{"internalType":"address","name":"spender","type":"address"}],"name":"ERC20InvalidSpender","type":"error"},{"inputs":[],"name":"EmergencyTreasuryBalanceNotZero","type":"error"},{"inputs":[],"name":"FailedInnerCall","type":"error"},{"inputs":[],"name":"InsufficientOlasBalance","type":"error"},{"inputs":[],"name":"InsufficientOlasStaked","type":"error"},{"inputs":[],"name":"InsufficientSigOlasBalance","type":"error"},{"inputs":[],"name":"InvalidAddress","type":"error"},{"inputs":[],"name":"InvalidUnstakeRequestId","type":"error"},{"inputs":[],"name":"NotOwnerOfUnstakeRequest","type":"error"},{"inputs":[],"name":"OnlyAdmin","type":"error"},{"inputs":[],"name":"OnlyAdminOrRelayer","type":"error"},{"inputs":[],"name":"OnlyRelayer","type":"error"},{"inputs":[],"name":"OverMaxThreshold","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"OwnableInvalidOwner","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"OwnableUnauthorizedAccount","type":"error"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"SafeERC20FailedOperation","type":"error"},{"inputs":[],"name":"StakersAllowList","type":"error"},{"inputs":[],"name":"TreasuryBalanceNotZero","type":"error"},{"inputs":[],"name":"UnstakeRequestFulfilled","type":"error"},{"inputs":[],"name":"UnstakeRequestNotFulfilled","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"newAdmin","type":"address"}],"name":"AdminUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"unstakeRequestId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"ClaimUnstakeRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"newEmergencyTreasury","type":"address"}],"name":"EmergencyTreasuryUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"newMaxThreshold","type":"uint256"}],"name":"MaxThresholdUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"nodeId","type":"uint256"},{"indexed":false,"internalType":"string","name":"nodeType","type":"string"},{"indexed":false,"internalType":"address","name":"agent","type":"address"},{"indexed":false,"internalType":"address","name":"operator","type":"address"}],"name":"NodeCreated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"newRelayer","type":"address"}],"name":"RelayerUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"treasuryAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"emergencyTreasuryAmount","type":"uint256"}],"name":"RewardedOlasAdded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"nodeId","type":"uint256"},{"indexed":false,"internalType":"address","name":"safeAddress","type":"address"}],"name":"SetSafeAddressForNode","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"nodeId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"serviceId","type":"uint256"}],"name":"SetServiceIdForNode","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"sigOlasAmount","type":"uint256"}],"name":"Stake","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"nodeId","type":"uint256"},{"indexed":false,"internalType":"enum OlasManager.NodeStatus","name":"status","type":"uint8"}],"name":"StatusUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"SystemPrivate","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"SystemPublic","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"newTreasury","type":"address"}],"name":"TreasuryUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"olasAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"unstakeRequestId","type":"uint256"}],"name":"UnstakeRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"unstakeRequestId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amountLocked","type":"uint256"}],"name":"UnstakeRequestUpdated","type":"event"},{"inputs":[],"name":"DENOMINATOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REWARD_FEE_PERCENTAGE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"stakers","type":"address[]"}],"name":"addStakersToAllowList","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"unstakeRequestId","type":"uint256"}],"name":"claimUnstakeRequest","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"emergencyTreasury","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"emergencyTreasuryFeePercentage","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"unstakeRequestId","type":"uint256"}],"name":"fillUnstakeRequest","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"isPublic","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"lockStaking","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"makePrivate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"makePublic","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"maxThreshold","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"nextNodeId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"nextUnstakeRequestId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"nodes","outputs":[{"internalType":"string","name":"nodeType","type":"string"},{"internalType":"enum OlasManager.NodeStatus","name":"status","type":"uint8"},{"internalType":"address","name":"agent","type":"address"},{"internalType":"address","name":"operator","type":"address"},{"internalType":"address","name":"safeAddress","type":"address"},{"internalType":"uint256","name":"serviceId","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"olasLocked","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"olasStaked","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"olasToken","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"putRewardedOlas","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"relayer","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"stakers","type":"address[]"}],"name":"removeStakersFromAllowList","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"nodeType","type":"string"},{"internalType":"address","name":"agent","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"runNode","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"safeAddresses","outputs":[{"internalType":"string","name":"nodeType","type":"string"},{"internalType":"enum OlasManager.NodeStatus","name":"status","type":"uint8"},{"internalType":"address","name":"agent","type":"address"},{"internalType":"address","name":"operator","type":"address"},{"internalType":"address","name":"safeAddress","type":"address"},{"internalType":"uint256","name":"serviceId","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_admin","type":"address"}],"name":"setAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_emergencyTreasury","type":"address"}],"name":"setEmergencyTreasury","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_relayer","type":"address"}],"name":"setRelayer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"nodeId","type":"uint256"},{"internalType":"address","name":"safeAddress","type":"address"}],"name":"setSafeAddressForNode","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"nodeId","type":"uint256"},{"internalType":"uint256","name":"serviceId","type":"uint256"}],"name":"setServiceIdForNode","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_treasury","type":"address"}],"name":"setTreasury","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"stakeToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"stakersAllowList","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"treasury","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"treasuryFeePercentage","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"unlockStaking","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"unstakeRequest","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"userAddress","type":"address"}],"name":"unstakeRequestInfosByStakerAddress","outputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"bool","name":"isClaimed","type":"bool"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"sigOlasAmount","type":"uint256"}],"internalType":"struct OlasManager.UnstakeRequestInfo[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"unstakeRequests","outputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"bool","name":"isClaimed","type":"bool"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"sigOlasAmount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"newMaxThreshold","type":"uint256"}],"name":"updateMaxThreshold","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"nodeId","type":"uint256"},{"internalType":"enum OlasManager.NodeStatus","name":"status","type":"uint8"}],"name":"updateStatus","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

TOKEN_CONTRACT_ADDRESS = '0x75A9174EbAdDc2D141917cCB738C330EA42E969D'
TOKEN_CONTRACT_ABI = '[{"inputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"symbol","type":"string"},{"internalType":"uint8","name":"decimals","type":"uint8"},{"internalType":"address","name":"owner","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"target","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]'


class Node:
    def __init__(self, name, shift, agent, operator, safe_address=None, service_id=None, contract_id=None):
        self.name = name
        self.shift = shift

        self.folder_name = name
        print(f'Node fodler: {self.folder_name}')

        self.agent = agent
        self.operator = operator

        self.contract_id = contract_id

        self.safe_address = safe_address
        self.service_id = service_id


class OlasManagerBackend:
    def __init__(self, owner_private, olas_token, contract, w3_gno, w3_sep):
        self.owner = w3_sep.eth.account.from_key(owner_private)
        self.olas_token = olas_token
        self.contract = contract
        self.w3_gno = w3_gno
        self.w3_sep = w3_sep

    def send_xdai(self, address, amount):
        print(self.w3_gno.eth.get_transaction_count(self.owner.address))
        tx = {
            'nonce': self.w3_gno.eth.get_transaction_count(self.owner.address),
            'from': self.owner.address,
            'to': address,
            'data': '0x',
            'value': self.w3_gno.to_wei(amount, 'ether'),
            'gasPrice': self.w3_gno.eth.gas_price,
        }
        tx['gas'] = self.w3_gno.eth.estimate_gas(tx)
        print(tx)

        signed_tx = self.owner.sign_transaction(tx)
        tx_hash = self.w3_gno.eth.send_raw_transaction(signed_tx.rawTransaction)
        self.w3_gno.eth.wait_for_transaction_receipt(tx_hash)

    def send_olas(self, address: str, amount):
        tx = self.olas_token.functions.transfer(address, self.w3_gno.to_wei(amount, 'ether')).build_transaction({
            'from': self.owner.address,
            'nonce': self.w3_gno.eth.get_transaction_count(self.owner.address),
        })
        print(tx)
        signed_tx = self.owner.sign_transaction(tx)
        tx_hash = self.w3_gno.eth.send_raw_transaction(signed_tx.rawTransaction)
        self.w3_gno.eth.wait_for_transaction_receipt(tx_hash)

    def clone_repo(self, node: Node):
        subprocess.run(['git', 'clone', 'https://github.com/valory-xyz/trader-quickstart.git'])
        shutil.move('trader-quickstart', node.folder_name)
        print('Cloned trader repo')

    def prepare_trader_config(self, node: Node):
        config_directory = os.path.join(node.folder_name, '.trader_runner')
        shutil.copytree('trader-runner-example', config_directory)

        os.remove(os.path.join(config_directory, 'service_safe_address.txt'))
        os.remove(os.path.join(config_directory, 'service_id.txt'))

        with open(os.path.join(config_directory, 'agent_address.txt'), 'w') as file:
            file.write(node.agent.address)

        with open(os.path.join(config_directory, 'agent_pkey.txt'), 'w') as file:
            file.write(self.w3_gno.to_hex(node.agent.key)[2:])

        with open(os.path.join(config_directory, 'keys.json'), 'w') as file:
            json.dump([{
                'address': node.agent.address,
                'private_key': self.w3_gno.to_hex(node.agent.key),
                'ledger': 'ethereum',
            }], file)

        with open(os.path.join(config_directory, 'operator_pkey.txt'), 'w') as file:
            file.write(self.w3_gno.to_hex(node.operator.key)[2:])

        with open(os.path.join(config_directory, 'operator_keys.json'), 'w') as file:
            json.dump([{
                'address': node.operator.address,
                'private_key': self.w3_gno.to_hex(node.operator.key),
                'ledger': 'ethereum',
            }], file)

    def send_deposits(self, node: Node):
        self.send_xdai(node.operator.address, 0.1)
        self.send_xdai(node.agent.address, 0.1)
        self.send_olas(node.operator.address, 20)

    def change_directories_owners(self, node: Node):
        build_dir = os.path.join(node.folder_name, 'trader', 'trader_service', f'abci_build_{node.shift}')
        subprocess.run(['sudo', 'chown', '-R', 'ubuntu:root', os.path.join(build_dir, 'agent_keys')])
        subprocess.run(['sudo', 'chown', '-R', 'ubuntu:root', os.path.join(build_dir, 'persistent_data')])

    def read_safe_address(self, node: Node) -> str:
        safe_file = os.path.join(node.folder_name, '.trader_runner', 'service_safe_address.txt')
        with open(safe_file, 'r') as file:
            safe_address = file.read()
        return safe_address

    def read_service_id(self, node: Node) -> str:
        safe_file = os.path.join(node.folder_name, '.trader_runner', 'service_id.txt')
        with open(safe_file, 'r') as file:
            service_id = file.read()
        return service_id

    def rename_build_directory(self, node: Node):
        old_path = os.path.join(node.folder_name, 'trader', 'trader_service', 'abci_build')
        new_path = os.path.join(node.folder_name, 'trader', 'trader_service', f'abci_build_{node.shift}')
        shutil.move(old_path, new_path)

    def update_compose(self, node: Node):
        compose_path = os.path.join(node.folder_name, 'trader', 'trader_service', f'abci_build_{node.shift}', 'docker-compose.yaml')
        with open(compose_path, 'r') as file:
            config = file.read()

        new_http_port = 8716 + node.shift
        config = config.replace('8716', f'{new_http_port}')

        lines = config.split('\n')
        new_lines = []

        for line in lines:
            if (
                'container_name' in line
                or 'networks' in line
                or 'service_trader_localnet' in line
                or 'ipv4_address' in line
            ):
                continue
            new_lines.append(line)
        config = '\n'.join(new_lines[:-6])

        with open(compose_path, 'w') as file:
            file.write(config)

    def autonomy_run(self, node: Node):
        subprocess.run([
            'poetry',
            'run',
            'autonomy',
            'deploy',
            'run',
            '--build-dir',
            f'trader_service/abci_build_{node.shift}',
            '--detach',
            '--no-recreate',
        ], cwd=f'{node.folder_name}/trader')

    def autonomy_stop(self, node: Node):
        subprocess.run([
            'poetry',
            'run',
            'autonomy',
            'deploy',
            'stop',
            '--build-dir',
            f'trader_service/abci_build_{node.shift}',
        ], cwd=f'{node.folder_name}/trader')

    def truncate_run_script(self, node: Node, lines: int):
        config_path = os.path.join(node.folder_name, 'run_service.sh')
        trunc_config_path = os.path.join(node.folder_name, 'trunc_run_service.sh')

        shutil.copy(config_path, trunc_config_path)
        with open(trunc_config_path, 'r') as file:
            config = file.read()
        config = '\n'.join(config.split('\n')[:-lines])
        with open(trunc_config_path, 'w') as file:
            file.write(config)

    def run_truncated_script(self, node: Node):
        subprocess.run(['./trunc_run_service.sh'], cwd=node.folder_name)

    def run_node(self, node: Node):
        self.clone_repo(node)


        self.prepare_trader_config(node)
        print('send_deposits')
        self.send_deposits(node)

        print('trunc_and_run 43')
        self.truncate_run_script(node, 43)
        self.run_truncated_script(node)

        node.safe_address = self.read_safe_address(node)
        print(f'Safe address: {node.safe_address}')
        self.send_xdai(node.safe_address, 1)

        node.service_id = self.read_service_id(node)
        print(f'Service id: {node.service_id}')

        print('trunc_and_run 5')
        self.truncate_run_script(node, 5)
        self.run_truncated_script(node)

        print('rename_build_directory')
        self.rename_build_directory(node)
        print('update_compose')
        self.update_compose(node)
        print('change_directories_owners')
        self.change_directories_owners(node)
        print('autonomy_run')
        self.autonomy_run(node)


def main():
    w3_gno = Web3(Web3.WebsocketProvider("wss://rpc.gnosischain.com/wss"))
    w3_sep = Web3(Web3.WebsocketProvider('wss://eth-sepolia.g.alchemy.com/v2/Qlr3apDsKG7I7tlI8YGwXtxDVeyT0Kzv'))
    manager = OlasManagerBackend(
        PRIVATE_KEY,
        w3_gno.eth.contract(address=OLAS_CONTRACT_ADDRESS, abi=OLAS_CONTRACT_ABI),
        w3_sep.eth.contract(address=OLAS_MANAGER_CONTRACT_ADDRESS, abi=OLAS_MANAGER_CONTRACT_ABI),
        w3_gno, w3_sep
    )
    token_contract = w3_sep.eth.contract(address=TOKEN_CONTRACT_ADDRESS, abi=TOKEN_CONTRACT_ABI)

    # stake
    stake_amount = manager.w3_sep.to_wei(20, "ether")
    print(stake_amount, type(stake_amount))
    contract_olas_locked_amount = manager.contract.functions.olasLocked().call()
    print(contract_olas_locked_amount, type(contract_olas_locked_amount))
    balance = token_contract.functions.balanceOf(OLAS_MANAGER_CONTRACT_ADDRESS).call()
    print(balance, type(balance))
    if token_contract.functions.balanceOf(OLAS_MANAGER_CONTRACT_ADDRESS).call() - contract_olas_locked_amount > stake_amount:
        tx = manager.contract.functions.lockStaking(stake_amount).build_transaction({
            "from": manager.owner.address,
            "nonce": w3_sep.eth.get_transaction_count(manager.owner.address)
        })
        print(tx)
        signed_tx = manager.owner.sign_transaction(tx)
        tx_hash = w3_sep.eth.send_raw_transaction(signed_tx.rawTransaction)
        w3_sep.eth.wait_for_transaction_receipt(tx_hash)

        agent = manager.w3_gno.eth.account.create()
        operator = manager.w3_gno.eth.account.create()
        print(f'Agent address: {agent.address}')
        print(f'Operator address: {operator.address}')

        node = Node(str(uuid.uuid4()), SHIFT, agent, operator)

        tx = manager.contract.functions.runNode(node.name, node.agent.address, node.operator.address).build_transaction({
            "from": manager.owner.address,
            "nonce": w3_sep.eth.get_transaction_count(manager.owner.address)
        })
        print(tx)
        signed_tx = manager.owner.sign_transaction(tx)
        tx_hash = w3_sep.eth.send_raw_transaction(signed_tx.rawTransaction)
        w3_sep.eth.wait_for_transaction_receipt(tx_hash)

        try:
            manager.run_node(node)

            tx = manager.contract.functions.setSafeAddressForNode(node.contract_id, node.safe_address).build_transaction({
                "from": manager.owner.address,
                "nonce": w3_sep.eth.get_transaction_count(manager.owner.address)
            })
            print(tx)
            signed_tx = manager.owner.sign_transaction(tx)
            tx_hash = w3_sep.eth.send_raw_transaction(signed_tx.rawTransaction)
            w3_sep.eth.wait_for_transaction_receipt(tx_hash)

            tx = manager.contract.functions.setServiceIdForNode(node.contract_id, node.service_id).build_transaction({
                "from": manager.owner.address,
                "nonce": w3_sep.eth.get_transaction_count(manager.owner.address)
            })
            print(tx)
            signed_tx = manager.owner.sign_transaction(tx)
            tx_hash = w3_sep.eth.send_raw_transaction(signed_tx.rawTransaction)
            w3_sep.eth.wait_for_transaction_receipt(tx_hash)

            tx = manager.contract.functions.updateStatus(node.contract_id, 1).build_transaction({
                "from": manager.owner.address,
                "nonce": w3_sep.eth.get_transaction_count(manager.owner.address)
            })
            print(tx)
            signed_tx = manager.owner.sign_transaction(tx)
            tx_hash = w3_sep.eth.send_raw_transaction(signed_tx.rawTransaction)
            w3_sep.eth.wait_for_transaction_receipt(tx_hash)
        except Exception as e:
            print(repr(e))


if __name__ == '__main__':
    main()
