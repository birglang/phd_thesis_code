// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

contract SDNFlowIntegrity {
    using ECDSA for bytes32;

    struct Proposal {
        uint256 id;
        address proposer;
        string flowDetails;
        bytes signature;
        bool verified;
        uint256 consensusScore;
    }

    struct Controller {
        address controllerAddress;
        uint256 reputation;
        uint256 trust;
        bool isRogue;
    }

    uint256 public proposalCounter;
    uint256 public consensusThreshold;
    mapping(uint256 => Proposal) public proposals;
    mapping(address => Controller) public controllers;
    address[] public controllerAddresses;
    mapping(address => bool) public isController;

    event ProposalCreated(uint256 id, address proposer, string flowDetails);
    event ProposalVerified(uint256 id, address verifier, bool status);
    event ConsensusReached(uint256 id, bool status);
    event ReputationUpdated(address controller, uint256 reputation);
    event TrustUpdated(address controller, uint256 trust);
    event RogueDevice(address controller, bool isRogue);

    constructor(address[] memory _controllers, uint256 _consensusThreshold) {
        for (uint256 i = 0; i < _controllers.length; i++) {
            controllers[_controllers[i]] = Controller({
                controllerAddress: _controllers[i],
                reputation: 100,
                trust: 100,
                isRogue: false
            });
            isController[_controllers[i]] = true;
        }
        controllerAddresses = _controllers;
        consensusThreshold = _consensusThreshold;
    }

    modifier onlyController() {
        require(isController[msg.sender], "Only controllers can call this function");
        _;
    }

    function createProposal(string memory _flowDetails, bytes memory _signature) public onlyController returns (uint256) {
        proposalCounter++;
        proposals[proposalCounter] = Proposal({
            id: proposalCounter,
            proposer: msg.sender,
            flowDetails: _flowDetails,
            signature: _signature,
            verified: false,
            consensusScore: 0
        });

        emit ProposalCreated(proposalCounter, msg.sender, _flowDetails);
        return proposalCounter;
    }

    function verifyProposal(uint256 _proposalId) public onlyController {
        Proposal storage proposal = proposals[_proposalId];
        require(proposal.id != 0, "Proposal does not exist");
        require(!proposal.verified, "Proposal already verified");
        require(!controllers[msg.sender].isRogue, "Rogue controller cannot verify");

        bool isValid = verifySignature(proposal.proposer, proposal.flowDetails, proposal.signature);
        proposal.consensusScore += isValid ? 1 : 0;

        emit ProposalVerified(_proposalId, msg.sender, isValid);
        updateReputationAndTrust(msg.sender, isValid);

        if (proposal.consensusScore >= (consensusThreshold * controllerAddresses.length) / 100) {
            proposal.verified = true;
            emit ConsensusReached(_proposalId, true);
        }
    }

    function verifySignature(address _proposer, string memory _flowDetails, bytes memory _signature) internal pure returns (bool) {
        bytes32 messageHash = keccak256(abi.encodePacked(_proposer, _flowDetails));
        bytes32 ethSignedMessageHash = messageHash.toEthSignedMessageHash();

        return ethSignedMessageHash.recover(_signature) == _proposer;
    }

    function updateReputationAndTrust(address _controller, bool _status) internal {
        Controller storage controller = controllers[_controller];
        if (_status) {
            controller.reputation += 10;
            controller.trust += 5;
        } else {
            controller.reputation -= 10;
            controller.trust -= 5;
            if (controller.reputation < 50) {
                controller.isRogue = true;
                emit RogueDevice(_controller, true);
            }
        }

        emit ReputationUpdated(_controller, controller.reputation);
        emit TrustUpdated(_controller, controller.trust);
    }

    function getProposal(uint256 _proposalId) public view returns (Proposal memory) {
        return proposals[_proposalId];
    }

    function getController(address _controllerAddress) public view returns (Controller memory) {
        return controllers[_controllerAddress];
    }

    function isRogueController(address _controllerAddress) public view returns (bool) {
        return controllers[_controllerAddress].isRogue;
    }
}
