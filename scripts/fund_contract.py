from brownie import DoubleOrNothing
from scripts.tools import amount


def fund_contract(amt, acct):
    game = DoubleOrNothing[-1]
    print("Funding game contract...")
    tx_transfer = acct.transfer(game, amount(amt))
    tx_transfer.wait(1)
    print(f"Funded game: {game} with {amount(amt)}.!")
