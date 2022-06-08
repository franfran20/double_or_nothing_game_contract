from brownie import DoubleOrNothing, network, config

from scripts.tools import (
    get_account,
    subscription_id,
    callback_gaslimit,
    numwords,
    request_confirmations,
)
from scripts.deploy.create_and_fund_subscription import (
    create_and_fund_subscription,
)
from scripts.fund_contract import fund_contract
from scripts.mock_fulfill_randomness import mock_fufill_randomness
from scripts.play_game import play_game
from scripts.tools import (
    LOCAL_ENV,
    get_account_balance,
    get_balance_contract,
)


def deploy_game(acct):
    if network.show_active() in LOCAL_ENV:
        # we mock the VRFCoordinator by deploying the contract 
        #creating a subscription and funding that subscription
        sub_id, vrf_mock = create_and_fund_subscription(acct)

        print("Deploying game contract....")
        game = DoubleOrNothing.deploy(
            sub_id,
            vrf_mock,
            config["networks"][network.show_active()]["keyhash"],
            callback_gaslimit,
            numwords,
            request_confirmations,
            {"from": acct},
        )
        print(f"Game deployed: {game}")
        return game, sub_id
    else:
        print("Deploying game contract....")
        game = DoubleOrNothing.deploy(
            subscription_id,
            config["networks"][network.show_active()]["vrf_coordinator"],
            config["networks"][network.show_active()]["keyhash"],
            callback_gaslimit,
            numwords,
            request_confirmations,
            {"from": acct, "required_confs": 3},
            publish_source=True,
        )
        print("Deployed")


def main():
    if network.show_active() in LOCAL_ENV:
        account = get_account()
    else: 
        account = get_account(id="Your encrypted id") #or your private key in your env

    #create and fund a subscription locally for your random number and deploy the game contract
    #and also deploy the game contract

    #when doing this on a live network you'll probably want to
    #create your subscription.
    #fund that subscription and add your contract as a consumer.
    #before even deploying the contract
    deploy_game(account)

    #fund contract for users to play game
    if network.show_active() in LOCAL_ENV:
        fund_contract(5, account)
    else:
        #we dont want to waste testet currency!
        fund_contract(0.0015, account)

    #check the contract balance to see if our fund reflected.
    get_balance_contract()

    
    # play game
    #now when testing locally we know that the request id 
    #increases by a value of 1 after every request. So lets make our life easier.

    if network.show_active() in LOCAL_ENV:
        #we play the game with three different accounts
        #and we'll see the different 4 outcomes printed out in our terminal
        play_game(0.2, account)
        mock_fufill_randomness(get_account(index=1), 1)
        play_game(0.1, account)
        mock_fufill_randomness(get_account(index=2), 2)
        play_game(0.5, account)
        mock_fufill_randomness(get_account(index=2), 3)
        play_game(0.5, account)
        mock_fufill_randomness(get_account(index=2), 4)
    else:
        play_game(0.1, account)

    #lets see the contract balance
    get_balance_contract()


    