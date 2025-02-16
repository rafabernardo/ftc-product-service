Feature: Identify a user with CPF

  Scenario: Cpf invalid format when trying to identify with CPF
    Given a non-existent user id "54768430007"
    When trying to add CPF "000"
    Then the response status code should be 422