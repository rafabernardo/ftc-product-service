Feature: Identify a user with CPF

  Scenario: User not found when trying to identify with CPF
    Given a non-existent user id "54768430007"
    When trying to add CPF "547.684.300-07"
    Then the response status code should be 404