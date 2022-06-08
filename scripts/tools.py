from brownie import accounts, network, DoubleOrNothing, config
from web3 import Web3

LOCAL_ENV = ["development", "hardhat", "ganache-local"]

# all values are based on the rinkeby network. Thats where our subscription was created!
subscription_id = 455
callback_gaslimit = 120000
numwords = 3
request_confirmations = 3


def get_account(id=None, index=None):
    if network.show_active() in LOCAL_ENV:
        return accounts[0]
    if id:
        return accounts.load(id)
    if index:
        return accounts[index]
    return config["wallets"]["from_key"]


def amount(amt):
    return Web3.toWei(amt, "ether")


def get_balance_contract():
    game = DoubleOrNothing[-1]
    print(f"Game contract balance: {game.balance()}")


def get_account_balance(acct):
    print(f"Player balance: {acct.balance()}")
    return acct.balance()


def get_random_words():
    game = DoubleOrNothing[-1]
    random_words_array = game.getRandomWords()
    for random_number in random_words_array:
        counter = 1
        print(f"Random number {counter}:{random_number}")
        counter += 1
