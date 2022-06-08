from brownie import Wei, network
import brownie
from scripts.deploy.deploy_and_run import deploy_game, fund_contract, get_balance_contract, play_game, mock_fufill_randomness
from scripts.tools import get_account, LOCAL_ENV, amount, get_account_balance
import pytest

def test_play_game():
    if network.show_active() not in LOCAL_ENV:
        pytest.skip("Only for local environment")
    account = get_account()
    AMOUNT_TO_FUND = 2
    # deploy mocks and contracts
    game, sub_id = deploy_game(account)
    # fund contract with 2 ether
    fund_contract(AMOUNT_TO_FUND, account)
    get_balance_contract()
    #fail on sending zero amount
    with brownie.reverts():
        play_game(0, account)
    #fail on sending more than half of contract balance
    with brownie.reverts():
        play_game((AMOUNT_TO_FUND/2), account)
    play_game(0.5, account)
    #we know the requestId locally
    request_id = game.s_requestId()
    assert game.requestIdToPlayer(request_id) == account.address
    assert game.requestIdToPlayerToAmount(request_id, account.address) == Wei("0.5 ether")

def test_mock_randomness():
    if network.show_active() not in LOCAL_ENV:
        pytest.skip("Only for local environment")
    account = get_account()
    AMOUNT_TO_FUND = 2
    # deploy mocks and contracts
    game, sub_id = deploy_game(account)
    # fund contract with 2 ether
    fund_contract(AMOUNT_TO_FUND, account)
    get_balance_contract()
    balance_before_gameplay = account.balance()
    play_game(0.4, account)
    # act like the chainlink node...
    tx_mock_fulfill = mock_fufill_randomness(account, 1)
    won_or_not = tx_mock_fulfill.events["played"]["won"]
    balance = get_account_balance(account)
    if won_or_not:
        assert balance == (balance_before_gameplay + amount(0.4))
    if not won_or_not:
        assert balance == (balance_before_gameplay - amount(0.4))