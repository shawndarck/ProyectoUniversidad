Feature: Ethereum Blockchain
 Scenario: Mine a block with 5 transactions
 Given I have 5 Ethereum nodes
 When I mine a block with 5 transactions
 Then the block should be added to the blockchain