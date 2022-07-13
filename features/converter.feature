Feature: Menu converter integration tests

	Scenario: Upload file test
      Given I have a csv file
	  When I upload the file
      Then The uploaded is successful

    Scenario: Get converted file test
      Given I have a uploaded a csv file
	  When I get the converted file
      Then The file is successfully converted

    Scenario: Delete file test
      Given I have a uploaded a csv file
	  When I delete the file
      Then The file is deleted successfully
