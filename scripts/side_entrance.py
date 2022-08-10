from scripts.helper.utils import *
from brownie import SideEntranceLenderPool

def main():
    ####################################################################
    ######### SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE #########
    ####################################################################

    # starting setup messages
    message('setup_start')

    # ether in pool
    ETHER_IN_POOL = ether_to_wei(100)

    # import accounts
    deployer, _fromDeployer, attacker, _fromAttacker = define_from_acc(qty=2)

    # deploy the contracts
    pool = SideEntranceLenderPool.deploy(_fromDeployer)

    # deposit into the pool
    pool.deposit(_fromDeployer | value_dict(ETHER_IN_POOL))

    # attacker initial ether balance
    ATTACKER_INITIAL_ETH_BALANCE = attacker.balance()

    # verify eth in pool
    assert pool.balance() == ETHER_IN_POOL

    # check if solved
    def solution_assertion():
        message('final_assertion_check')
        try:

            ############################################
            ############ SUCCESS CONDITIONS ############
            ############################################
            # Not checking exactly how much is the final balance of the attacker,
            # because it'll depend on how much gas the attacker spends in the attack
            # If there were no gas costs, it would be balance before attack + ETHER_IN_POOL
            assert pool.balance() == 0
            assert attacker.balance() == ATTACKER_INITIAL_ETH_BALANCE
            return True
        except:
            return False

    # done setting up
    message('setup_end')
    message('solution_start')
# #########################################################
# A surprisingly simple lending pool allows anyone to deposit ETH, and withdraw it at any point in time.
#
# This very simple lending pool has 1000 ETH in balance already, and is offering free flash loans using the deposited ETH to promote their system.
#
# You must take all ETH from the lending pool. 
# #########################################################

    #############################
    ##### SOLUTION GOES HERE ####
    #############################

        

###############################################################
###################### CHECKING SOLUTION ######################
###############################################################
    message('solution_end')
    print(f'Challenge is solved: {solution_assertion()}')
