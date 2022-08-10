from scripts.helper.utils import *
from brownie import DamnValuableTokenSnapshot, SimpleGovernance, SelfiePool

def main():
    ####################################################################
    ######### SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE #########
    ####################################################################


    # starting setup messages
    message('setup_start')

    # tokens in pool and token initial supply
    TOKENS_IN_POOL = ether_to_wei(1500000)
    TOKEN_INITIAL_SUPPLY = ether_to_wei(2000000)

    # import accounts
    deployer, _fromDeployer, attacker, _fromAttacker = define_from_acc(qty=2)

    # deploy the contracts
    token = DamnValuableTokenSnapshot.deploy(TOKEN_INITIAL_SUPPLY, _fromDeployer)
    governance = SimpleGovernance.deploy(token.address, _fromDeployer)
    pool = SelfiePool.deploy(token.address, governance.address, _fromDeployer)

    # fund the pool
    token.transfer(pool.address, TOKENS_IN_POOL, _fromDeployer)

    # confirm the balances are correct
    assert token.balanceOf(pool.address) == TOKENS_IN_POOL

    # check if solved
    def solution_assertion():
        message('final_assertion_check')
        try:

            ############################################
            ############ SUCCESS CONDITIONS ############
            ############################################
            # Attacker has taken all tokens from the pool
            assert token.balanceOf(attacker.address) == TOKENS_IN_POOL
            assert token.balanceOf(pool.address) == 0
            return True
        except:
            return False

    # done setting up
    message('setup_end')
    message('solution_start')
# #########################################################
# A new cool lending pool has launched! It's now offering flash loans of DVT tokens.
#
# Wow, and it even includes a really fancy governance mechanism to control it.
#
# What could go wrong, right ?
#
# You start with no DVT tokens in balance, and the pool has 1.5 million. Your objective: take them all.
# #########################################################

    #############################
    ##### SOLUTION GOES HERE ####
    #############################

        

###############################################################
###################### CHECKING SOLUTION ######################
###############################################################
    message('solution_end')
    print(f'Challenge is solved: {solution_assertion()}')
