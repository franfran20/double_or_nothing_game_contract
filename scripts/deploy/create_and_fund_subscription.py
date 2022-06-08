from brownie import VRFCoordinatorV2Mock
from scripts.tools import amount


def create_and_fund_subscription(acct):
    print("Deploying VRFMOCK...")
    # The base fee is the minimum amount of link you're willing to pay for a request?
    # The gas_price_link is the amount of link per gas 1e9?
    vrf_mock = VRFCoordinatorV2Mock.deploy(amount(0.1), 1000000000, {"from": acct})
    print(f"Mock deployed: {vrf_mock}")

    print("Creating subscription...")
    tx_create = vrf_mock.createSubscription({"from": acct})
    subId = tx_create.return_value
    print(f"subscription Id: {subId}")

    print("Funding subscription...")
    vrf_mock.fundSubscription(subId, amount(3), {"from": acct})
    print("Subscription Funded!")
    return subId, vrf_mock
    
