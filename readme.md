To Run the App:
- create a Json file with the claim and policy you wish to use
- navigate to the project folder in a command line
- run `.\.venv\Scripts\python.exe src\insurance_claims\app.py [LOCAL_PATH_TO_FILE]`


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

