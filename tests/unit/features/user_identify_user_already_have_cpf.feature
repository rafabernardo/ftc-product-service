Feature: Identify a user with CPF

  Scenario: User already have cpf when trying to identify with CPF
    Given a user with id "67a77edeaf970c68f41cc3d3"
    When trying to add CPF "547.684.300-07"
    Then the response status code should be 422