package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/json"
	"fmt"
	"strconv"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// SmartContract provides functions for managing a blockchain-based SDN proposal verification system
type SmartContract struct {
	contractapi.Contract
}

// Controller represents an SDN controller
type Controller struct {
	ID         string  `json:"id"`
	Domain     string  `json:"domain"`
	TrustScore float64 `json:"trustScore"`
	Status     string  `json:"status"` // "trusted", "suspected", "rogue"
}

// Proposal represents a flow modification proposal
type Proposal struct {
	ID          string `json:"id"`
	SourceIP    string `json:"sourceIp"`
	DestinationIP string `json:"destinationIp"`
	InPort      string `json:"inPort"`
	SrcMAC      string `json:"srcMac"`
	DstMAC      string `json:"dstMac"`
	Action      string `json:"action"`
	Priority    int    `json:"priority"`
	Hash        string `json:"hash"`
}

// AddController adds a new controller to the ledger
func (s *SmartContract) AddController(ctx contractapi.TransactionContextInterface, id string, domain string) error {
	controller := Controller{
		ID:         id,
		Domain:     domain,
		TrustScore: 1.0,
		Status:     "trusted",
	}
	controllerJSON, err := json.Marshal(controller)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(id, controllerJSON)
}

// SubmitProposal submits a new proposal to the ledger
func (s *SmartContract) SubmitProposal(ctx contractapi.TransactionContextInterface, id string, sourceIp string, destinationIp string, inPort string, srcMac string, dstMac string, action string, priority int) error {
	proposal := Proposal{
		ID:            id,
		SourceIP:      sourceIp,
		DestinationIP: destinationIp,
		InPort:        inPort,
		SrcMAC:        srcMac,
		DstMAC:        dstMac,
		Action:        action,
		Priority:      priority,
		Hash:          s.calculateHash(id, sourceIp, destinationIp, inPort, srcMac, dstMac, action, priority),
	}
	proposalJSON, err := json.Marshal(proposal)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(id, proposalJSON)
}

// VerifyProposal verifies a proposal's digital signature, participating controllers, and consensus
func (s *SmartContract) VerifyProposal(ctx contractapi.TransactionContextInterface, id string, domain string) (bool, error) {
	proposalJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return false, err
	}
	if proposalJSON == nil {
		return false, fmt.Errorf("proposal not found: %s", id)
	}

	var proposal Proposal
	err = json.Unmarshal(proposalJSON, &proposal)
	if err != nil {
		return false, err
	}

	// Stage I: Verify proposal's hash
	expectedHash := s.calculateHash(proposal.ID, proposal.SourceIP, proposal.DestinationIP, proposal.InPort, proposal.SrcMAC, proposal.DstMAC, proposal.Action, proposal.Priority)
	if proposal.Hash != expectedHash {
		return false, fmt.Errorf("proposal hash mismatch")
	}

	// Stage II: Verify participating controllers
	validControllers, err := s.getValidControllers(ctx, domain)
	if err != nil {
		return false, err
	}
	if len(validControllers) == 0 {
		return false, fmt.Errorf("no valid controllers available")
	}

	// Stage III: PBFT consensus
	isValid, err := s.VotingConsensus(ctx, validControllers, proposal)
	if err != nil {
		return false, err
	}

	if !isValid {
		// Update trust scores
		err = s.updateTrustScores(ctx, validControllers, false)
		if err != nil {
			return false, err
		}
		return false, nil
	}

	// Proposal is valid
	err = s.updateTrustScores(ctx, validControllers, true)
	if err != nil {
		return false, err
	}

	return true, nil
}

// calculateHash calculates the hash of a proposal
func (s *SmartContract) calculateHash(id string, sourceIp string, destinationIp string, inPort string, srcMac string, dstMac string, action string, priority int) string {
	hashInput := id + sourceIp + destinationIp + inPort + srcMac + dstMac + action + strconv.Itoa(priority)
	hash := sha256.New()
	hash.Write([]byte(hashInput))
	return fmt.Sprintf("%x", hash.Sum(nil))
}

// getValidControllers returns a list of valid controllers in a domain
func (s *SmartContract) getValidControllers(ctx contractapi.TransactionContextInterface, domain string) ([]Controller, error) {
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var controllers []Controller
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var controller Controller
		err = json.Unmarshal(queryResponse.Value, &controller)
		if err != nil {
			return nil, err
		}

		if controller.Domain == domain && controller.Status != "rogue" {
			controllers = append(controllers, controller)
		}
	}

	return controllers, nil
}

// PBFTConsensus performs PBFT consensus among controllers
func (s *SmartContract) VotingConsensus(ctx contractapi.TransactionContextInterface, controllers []Controller, proposal Proposal) (bool, error) {
	n := len(controllers)
	f := (n - 1) / 3
	validVotes := 0

	for _, controller := range controllers {
		// Simulate independent proposal verification by each controller
		if s.verifyProposalIndependently(proposal) {
			validVotes++
		}
	}

	if validVotes >= (2*f + 1) {
		return true, nil
	}

	return false, nil
}

// verifyProposalIndependently simulates a controller independently verifying a proposal
func (s *SmartContract) verifyProposalIndependently(proposal Proposal) bool {
	// Recalculate the hash and compare
	expectedHash := s.calculateHash(proposal.ID, proposal.SourceIP, proposal.DestinationIP, proposal.InPort, proposal.SrcMAC, proposal.DstMAC, proposal.Action, proposal.Priority)
	return proposal.Hash == expectedHash
}

// updateTrustScores updates the trust scores of controllers based on the proposal verification outcome
func (s *SmartContract) updateTrustScores(ctx contractapi.TransactionContextInterface, controllers []Controller, isValid bool) error {
	for _, controller := range controllers {
		if !isValid {
			controller.TrustScore -= 0.1
		}

		if controller.TrustScore < 0.6 {
			controller.Status = "rogue"
		} else if controller.TrustScore < 1.0 {
			controller.Status = "suspected"
		} else {
			controller.Status = "trusted"
		}

		controllerJSON, err := json.Marshal(controller)
		if err != nil {
			return err
		}

		err = ctx.GetStub().PutState(controller.ID, controllerJSON)
		if err != nil {
			return err
		}
	}

	return nil
}

func main() {
	chaincode, err := contractapi.NewChaincode(new(SmartContract))
	if err != nil {
		fmt.Printf("Error create chaincode: %s", err.Error())
		return
	}

	if err := chaincode.Start(); err != nil {
		fmt.Printf("Error starting chaincode: %s", err.Error())
	}
}
