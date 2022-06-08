//SPDX-License-Identifier: MIT

pragma solidity ^0.8.4;

import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";

/// @title A doubke or nothing game contract.
/// @author Egboluche Francis
/// @notice Users stand a chance to win double rewards
/// @dev The contract uses chainlinkVRF to get random numbers.

error InsufficientBalance(uint256 balance);

contract DoubleOrNothing is VRFConsumerBaseV2 {
    VRFCoordinatorV2Interface immutable COORDINATOR;
    address private immutable s_vrf_coordinator;
    bytes32 private immutable s_keyHash;
    bool[2] public constant DECIDER = [true, false];
    uint16 private immutable s_requestConfirmations;
    uint32 public s_callBackGasLimit;
    uint32 private immutable numWords;
    uint64 public s_subscriptionId;
    uint256 public s_requestId;
    uint256[] public s_randomWords;
    mapping(uint256 => address) public requestIdToPlayer;
    mapping(uint256 => mapping(address => uint256))
        public requestIdToPlayerToAmount;

    event played(
        address indexed player,
        uint256 indexed amount,
        bool indexed won
    );

    constructor(
        uint64 _subscriptionId,
        address _vrfCoordinator,
        bytes32 _keyhash,
        uint32 _callBackGasLimit,
        uint32 _numWords,
        uint16 requestConfirmations
    ) VRFConsumerBaseV2(_vrfCoordinator) {
        s_subscriptionId = _subscriptionId;
        s_vrf_coordinator = _vrfCoordinator;
        COORDINATOR = VRFCoordinatorV2Interface(_vrfCoordinator);
        s_keyHash = _keyhash;
        s_callBackGasLimit = _callBackGasLimit;
        numWords = _numWords;
        s_requestConfirmations = requestConfirmations;
    }

    /// @notice Users will be able to play the game with this function
    /// @dev A request for a random number to a chainlink node is initiated

    function playGame() public payable {
        require(msg.value > 0, "Invalid Amount");
        uint256 balance = (address(this).balance - msg.value);
        if (balance <= (msg.value * 2)) {
            revert InsufficientBalance(address(this).balance);
        }
        uint256 requestId = COORDINATOR.requestRandomWords(
            s_keyHash,
            s_subscriptionId,
            s_requestConfirmations,
            s_callBackGasLimit,
            numWords
        );
        requestIdToPlayer[requestId] = msg.sender;
        requestIdToPlayerToAmount[requestId][msg.sender] = msg.value;
        s_requestId = requestId;
    }

    /// @notice Contains all the logic for the deciding the outcome
    /// @dev The chainlink Node calls this function wuth the logic.
    /// @param request_id The request id specified by the chainlink node for a particular request
    /// @param randomWords An array of random numbers populated to us by the chainlink node

    function fulfillRandomWords(
        uint256 request_id,
        uint256[] memory randomWords
    ) internal override {
        s_randomWords = randomWords;
        // we requested 3 random numbers here to help ease our unit tests with mocks.
        // so we have a varierty to of random numbers to choose from by just changing the RNG we choose here.
        uint256 randomNum = (s_randomWords[2] % 2);
        if (DECIDER[randomNum] == true) {
            address player = requestIdToPlayer[request_id];
            //double the amount
            uint256 amount = requestIdToPlayerToAmount[request_id][player] * 2;
            //send double, they won fair and square
            (bool sent, ) = payable(player).call{value: amount}("");
            require(sent, "Failed to send rewards!");
            emit played(player, (amount / 2), true);
        }
        if (DECIDER[randomNum] == false) {
            address player = requestIdToPlayer[request_id];
            uint256 amount = requestIdToPlayerToAmount[request_id][player];
            emit played(player, amount, false);
        }
    }

    function getRandomWords() public view returns (uint256[] memory) {
        return s_randomWords;
    }

    receive() external payable {}
}
