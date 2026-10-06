To Run the App:
- create a Json file with the claim and policy you wish to use
- navigate to the project folder in a command line
- TODO: INSERT COMMAND TO RUN

===================
Commit 1: Project Setup

- Initialized a python project with pytest and json related packages
- Created a blank "Claims Processor" class meant to house the whole app
    - Populated with unimplemented methods just so I have something to call when writing unit tests
- Created a pytest file, created one simple test that fails in the current state, but should later succeed

Use of Json: decided to use json for input so that tests are quick to make/update. If I want to test on the same input in a few different tests, I can without it crowding up a code file or duplicating the same lines.

