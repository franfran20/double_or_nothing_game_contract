from brownie import DoubleOrNothing, VRFCoordinatorV2Mock

# acting as a chainlink node...
def mock_fufill_randomness(acct, request_id):
    mock = VRFCoordinatorV2Mock[-1]
    game = DoubleOrNothing[-1]
    # mock fulfillrandomness
    print("mocking fulfill randomness...")
    tx_mock_fulfill = mock.fulfillRandomWords(request_id, game, {"from": acct})
    tx_mock_fulfill.wait(1)
    # when the chainlink node responds it calls our contract and emits an event
    won_or_not = tx_mock_fulfill.events["played"]["won"]
    playedAmt = tx_mock_fulfill.events["played"]["amount"]
    print(f"Won: {won_or_not}, Amount: {playedAmt}")
    print("Yipee-kay-Yay!")
    #tx_mock_fulfill.info()
    return tx_mock_fulfill
