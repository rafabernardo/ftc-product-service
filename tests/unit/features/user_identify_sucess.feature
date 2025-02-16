Feature: Identify a user with CPF

  Scenario: User wants to identify themselves with CPF
    Given a user with id "67a77edeaf970c68f41cc3d3"
    When the user wants to add their CPF "547.684.300-07"
    Then the user should have the CPF "54768430007"
    And the response status code should be 200