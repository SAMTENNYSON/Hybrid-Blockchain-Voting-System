// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Voting {
    address public owner;

    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

    mapping(uint => Candidate) public candidates;
    
    // CHANGE 1: We now map a "String ID" (Biometric Hash) to a boolean
    mapping(string => bool) public voters; 
    
    uint public candidatesCount;

    constructor() {
        owner = msg.sender;
        addCandidate("Candidate A (Party 1)");
        addCandidate("Candidate B (Party 2)");
    }

    function addCandidate (string memory _name) public {
        require(msg.sender == owner, "Only admin can add candidates.");
        candidatesCount ++;
        candidates[candidatesCount] = Candidate(candidatesCount, _name, 0);
    }

    // CHANGE 2: We accept the voter's unique ID as an argument
    function vote (uint _candidateId, string memory _voterId) public {
        // Check if this specific Identity has voted
        require(!voters[_voterId], "This Identity has already voted.");

        require(_candidateId > 0 && _candidateId <= candidatesCount, "Invalid candidate ID.");

        // Mark this Identity as voted
        voters[_voterId] = true;

        candidates[_candidateId].voteCount ++;
    }
}