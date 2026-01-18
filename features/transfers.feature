Feature: Transfers
    Scenario: User is able to make outgoing transfer
        Given Account registry is empty
        And I create an account using name: "krishna", last name: "krishna", pesel: "79101011234"
        When I make "incoming" transfer of "500" from pesel "79101011234"
        When I make "outgoing" transfer of "500" from pesel "79101011234"
        Then The transfer should be accepted
        Then The balance of account with pesel "79101011234" should be "0"

    Scenario: User is able to take incoming transfer
        Given Account registry is empty
        And I create an account using name: "krishna", last name: "krishna", pesel: "79101011234"
        When I make "incoming" transfer of "500" from pesel "79101011234"
        Then The transfer should be accepted
        Then The balance of account with pesel "79101011234" should be "500"

    Scenario: User is unable to make outgoing transfer with insufficient account
        Given Account registry is empty
        And I create an account using name: "krishna", last name: "krishna", pesel: "79101011234"
        When I make "incoming" transfer of "100" from pesel "79101011234"
        When I make "outgoing" transfer of "500" from pesel "79101011234"
        Then The transfer should be rejected
        Then The balance of account with pesel "79101011234" should be "100"

    Scenario: User is able to make express transfer
        Given Account registry is empty
        And I create an account using name: "krishna", last name: "krishna", pesel: "79101011234"
        When I make "incoming" transfer of "1000" from pesel "79101011234"
        When I make "express" transfer of "500" from pesel "79101011234"
        Then The transfer should be accepted
        Then The balance of account with pesel "79101011234" should be "499"