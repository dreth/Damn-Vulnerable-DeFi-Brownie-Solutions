from scripts.helper.utils import *
from brownie import ClimberTimelock, ClimberVault, DamnValuableToken

def main():
    ####################################################################
    ######### SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE #########
    ####################################################################


    # starting setup messages
    message('setup_start')

    # Vault starts with 10 million tokens
    VAULT_TOKEN_BALANCE = ether_to_wei(10000000)

    # import accounts
    deployer, _fromDeployer, proposer, _fromProposer, sweeper, _fromSweeper, attacker, _fromAttacker = define_from_acc(qty=4)

    # set attacker balance to 0.1 ETH
    set_account_balance_network(attacker.address, hex(ether_to_wei(0.1)))
    # check attacker balance
    assert attacker.balance() == ether_to_wei(0.1)

    # Deploy the vault behind a proxy using the UUPS pattern,
    # passing the necessary addresses for the `ClimberVault::initialize(address,address,address)` function
    ERC1967ProxyABI, ERC1967ProxyBytecode = load_abi_and_bytecode_json('built_helper_contracts/build-erc-1967-proxy/ERC1967Proxy.json')
    vault = ClimberVault.deploy(_fromDeployer)
    initialization_data = vault.initialize.encode_input(deployer.address, proposer.address, sweeper.address)
    proxy = load_contract_from_abi_and_bytecode('ERC1967Proxy', ERC1967ProxyABI, ERC1967ProxyBytecode, constructor_params=[(vault.address, 'address'), (initialization_data, 'bytes')])
    proxy_vault = Contract.from_abi("Vault", proxy.address, vault.abi)

    # check if everything is set up properly
    assert proxy_vault.getSweeper() == sweeper.address
    assert proxy_vault.getLastWithdrawalTimestamp() > 0
    assert proxy_vault.owner() != ZERO_ADDRESS
    assert proxy_vault.owner() != deployer.address

    # Instantiate timelock
    timelockAddress = proxy_vault.owner()
    timelock = ClimberTimelock.at(timelockAddress)
        
    # Ensure timelock roles are correctly initialized
    assert timelock.hasRole(timelock.PROPOSER_ROLE(), proposer.address) == True
    assert timelock.hasRole(timelock.ADMIN_ROLE(), deployer.address) == True

    # Deploy token and transfer initial token balance to the vault
    token = DamnValuableToken.deploy(_fromDeployer)
    token.transfer(proxy_vault.address, VAULT_TOKEN_BALANCE, _fromDeployer)

    # check the balance is correct
    assert token.balanceOf(proxy_vault.address) == VAULT_TOKEN_BALANCE

    # check if solved
    def solution_assertion():
        message('final_assertion_check')
        try:

            ############################################
            ############ SUCCESS CONDITIONS ############
            ############################################
            assert token.balanceOf(proxy_vault.address) == 0
            assert token.balanceOf(attacker.address) == VAULT_TOKEN_BALANCE
            return True
            
        except:
            return False

    # done setting up
    message('setup_end')
    message('solution_start')
# #########################################################
# There's a secure vault contract guarding 10 million DVT tokens. The vault is upgradeable, following the UUPS pattern.
#
# The owner of the vault, currently a timelock contract, can withdraw a very limited amount of tokens every 15 days.
#
# On the vault there's an additional role with powers to sweep all tokens in case of an emergency.
#
# On the timelock, only an account with a "Proposer" role can schedule actions that can be executed 1 hour later.
#
# Your goal is to empty the vault. 
# #########################################################

    #############################
    ##### SOLUTION GOES HERE ####
    #############################

        

###############################################################
###################### CHECKING SOLUTION ######################
###############################################################
    message('solution_end')
    print(f'Challenge is solved: {solution_assertion()}')
