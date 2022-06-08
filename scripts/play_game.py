from brownie import DoubleOrNothing
from scripts.tools import amount


def play_game(amt, acct):
    print(f"{acct.address} playing game....")
    game = DoubleOrNothing[-1]
    # so we can have a better idea if they won or not
    # p.s test cover this already..
    print(f"player previous balance: {acct.balance()}")
    tx = game.playGame({"from": acct, "value": amount(amt)})
    tx.wait(1)
    print(f"Game played with {acct.address} with amount: {amount(amt)}")
