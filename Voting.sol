// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Voting {
    address public owner;

    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

    // Store candidates
    mapping(uint => Candidate) public candidates;
    // Store voters status (has voted or not)
    mapping(address => bool) public voters;
    // Count of candidates
    uint public candidatesCount;

    constructor() {
        owner = msg.sender; // The account that deploys this is the 'Admin'
        // Add two default candidates for the demo
        addCandidate("Candidate A (Party 1)");
        addCandidate("Candidate B (Party 2)");
    }

    // Function to add a candidate (Only Admin can call this)
    function addCandidate (string memory _name) public {
        require(msg.sender == owner, "Only admin can add candidates.");
        candidatesCount ++;
        candidates[candidatesCount] = Candidate(candidatesCount, _name, 0);
    }

    // Function to cast a vote
    function vote (uint _candidateId) public {
        // Check 1: Voter has not voted before
        require(!voters[msg.sender], "You have already voted.");

        // Check 2: Candidate ID is valid
        require(_candidateId > 0 && _candidateId <= candidatesCount, "Invalid candidate ID.");

        // Record the vote
        voters[msg.sender] = true;

        // Update the count
        candidates[_candidateId].voteCount ++;
    }
}