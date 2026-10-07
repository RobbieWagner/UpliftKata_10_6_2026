To Run the App:
- create a Json file with the claim and policy you wish to use
- navigate to the project folder in a command line
- run `.\.venv\Scripts\python.exe src\insurance_claims\app.py [LOCAL_PATH_TO_FILE]`

===================
Commit 8: Implement Coverage Limits

- all unit tests pass
- coverage limits set properly

===================
Commit 7: Coverage Limit Tests

- create a unit test for coverage limits

===================
Commit 6: First Implementation of Evaluate Claim

- evaluate the claim based on the first 4 business rules
- ensure tests pass

Next commit, I will create unit tests around the coverage limit amount. I will be assuming that the policy is still approved, but payout will not be higher than coverage limit

===================
Commit 5: Claim Approval/Denial tests

- create tests to test all business rules dealing with approving vs denying a claim.
- create unit tests for the basic rule "Payout = `amountClaimed - deductible`" since it will effect unit tests later if I dont account for it now

A few decisions made: 
Claims with incident dates equal to the start or end date will be APPROVED
If payout is 0, claim should be DENIED on top of the zero payout reason code
Assuming no reasonCode takes precedence over another. If there are two reasons for denial, exact reasonCode provided doesn't matter

===================
Commit 4: Pass policy decision logic tests

- Make sure the correct policy to apply is chosen
- Make sure errors are thrown when the policy cannot be found

=================== 
Commit 3: Readjusting Input Handling, more unit tests

- Readjusted Input Handling to only take in an insurance claim since that seems to be more aligned with the spirit of this Kata.
- Created a few new unit tests to cover what I will implement next. Need to make sure lists of policies are loaded in correct, and the correct policy is used

Had to pivot a bit since the direction this app was going was incorrect. Changed my mind about how to send in claims, leading to some rework and somewhat drifting away from best practices, in the next commits, I will focus on more incremental changes, and writing more unit tests.

===================
Commit 2 : Pass first tests

- Implemented argument gathering to make the app runnable outside of tests (helpful to run specific tests manually).
- Hardcode policy, claim, and evaluation results to pass first 3 tests.

In the next few commits, I will create more tests outside of this policy/claims setup, and then reevaluate input handling. I think I will have policies defined on the backend, and have users just input claims to better mock real world scenarios.


===================
Commit 1: Project Setup

- Initialized a python project with pytest and json related packages
- Created a blank "Claims Processor" class meant to house the whole app
    - Populated with unimplemented methods just so I have something to call when writing unit tests
- Created a pytest file, created one simple test that fails in the current state, but should later succeed

Use of Json: decided to use json for input so that tests are quick to make/update. If I want to test on the same input in a few different tests, I can without it crowding up a code file or duplicating the same lines.

