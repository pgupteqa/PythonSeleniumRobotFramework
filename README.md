
# Salesforce UI Automation using RobotFramework Selenium and Python

This is a **Salesforce UI automation framework** developed using **RobotFramework**, **Python**, **Selenium Library** 
It is designed to support cross-browser testing with **LambdaTest**, nightly CI/CD integration using **GitHub Actions** (In-Progress), and supports **data-driven testing** using various **JSON** files.

The framework supports:
- Execution with RobotFramework
- Cross-browser testing on local & cloud (LambdaTest)
- Retry Analyzer for flaky tests using RobotFramework RetryFailed Listener
- Headless execution for faster test runs
- CI/CD integration with GitHub Actions (in-progress)

## About Me

- Hi, my name is Pratik Gupte and I have 8 years of experience working as a QA Engineer, including 3 years in Automation Testing using tools like Selenium Webdriver,RobotFramework, Copado Robotic Testing.
Currently expanding my skills learning the API Testing using Python Requests Library and Performance Testing.


## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://github.com/pgupteqa/)

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pratik-gupte-19145156/)



## Prerequisites

Before running this framework, ensure the following software is installed on your system:
- Python Latest Version
- RobotFramework
- robotframework-datadriver
- robotframework-pabot
- robotframework-seleniumlibrary
- robotframework-retryfailed
- simple-salesforce (REST API Client)
- python-dotenv (To Read Environment Variables)
- allure-robotframework

## Key Features

- Page Object Model (POM) design pattern
- JSON-based data-driven test approach
- Cross-browser support (Chrome, Firefox, Edge, etc.)
- LambdaTest cloud integration for cross-platform/browser runs
- Headless Runs with chrome, firefox and edge
- Retry mechanism for flaky tests
- Parallel execution with pabot
- Allure report generation
- Screenshots on failure

## Tech Stack

- **Language**: Python, RobotFramework
- **Automation**: RobotFramework Selenium Library
- **Test Framework**: RobotFramework Latest Version
- **Cloud Grid**: LambdaTest
- **CI/CD**: GitHub Actions
- **Reporting**: Allure Reports

## Setup Instruction

**Clone the Repository**

```bash
  git clone https://github.com/pgupteqa/PythonSeleniumRobotFramework.git
  cd PythonSeleniumRobotFramework

```

**Running Tests on Local Machine**

- **Running as Robot Test**:

```bash
  robot --listener allure_robotframework:allure-results  --variable browser:chrome --variable headless:false --variable envname:QA --variable islambda:false -i e2elead Tests/

```

**Running Tests on Local Machine in HeadLess Mode**

```bash
 robot --listener allure_robotframework:allure-results  --variable browser:chrome --variable headless:true --variable envname:QA --variable islambda:false -i e2elead Tests/

```
**Running Tests on LambdaTest**

```bash
 robot --listener allure_robotframework:allure-results  --variable browser:chrome --variable headless:false --variable envname:QA --variable islambda:true -i e2elead Tests/

```

**Retry Analyzer for Flaky Tests**:
```bash
 robot --listener allure_robotframework:allure-results --listener RetryFailed  --variable browser:chrome --variable headless:false --variable envname:QA --variable islambda:false -i e2elead Tests/
 
```
**Parallel Running**:

```bash
pabot --processes 4 --testlevelsplit --listener allure_robotframework:allure-results --listener RetryFailed  --variable browser:chrome --variable headless:false --variable envname:QA --variable islambda:false -i e2elead Tests/
 
```

**Generate Allure Reports**:
```bash
 allure generate allure-results
 allure open allure-report
```








    
## Project Files Structure

```bash

├─ README.md
├─ Resources/ # Commomn Robot file and decleration of Variables
├─ Page Objects #Page object python modules (POM)
├─ Custom Library # Created custom Libraries of Common Utility for Browsers selection, Salesforce API
├─ Tests/ # Robot test suites (.robot)
├─ data/
│ └─ loginTestData.json # JSON files for data-driven tests
├─ Screenshots #Store failed test screenshot
├─ allure-report

```


## Example Robot TestCase:

```bash

*** Settings ***
Resource    ../Resources/Common.robot

Test Setup    Run Keywords  Open SF Login Page  Setup Lead E2E Test Data
Test Teardown    Close Browser Session
Test Tags     smoke   regression  e2elead   test:retry(2)

*** Test Cases ***
E2E Lead To Opportunity Flow
    [Documentation]     This is a e2e Lead to Opportunity conversion test
    Login to salesforce     username=${validusername}     password=${validpassword}
    Validate app launcher icon
    Go To Leads App
    Create Lead Record and Get Lead Lastname
    Validate lead status should be    Open - Not Contacted
    Convert Lead
    Validate Created Contact Record   ${contactleadname}
    Navigate To Contact After Lead Conversion    ${envname}

*** Keywords ***
Create Lead Record and Get Lead Lastname
    ${contactleadname}  Create new lead record    ${leadrecorddata}
    Set suite variable    ${contactleadname}


```
## Reports & Logs

- Reports: After execution, a detailed HTML report will be generated at allure-report
- The report contains information on test cases executed, passed, failed, and skipped, along with screenshots for failed tests.

## Logs:
- Logs are created during the test execution and stored in the report as keywords.

## LambdaTest Integration

To run tests on the cloud:
- Set the following environment variables (or GitHub Secrets):

```bash
LT_USERNAME
LT_ACCESS_KEY

```

- Note: In this POC I have used the GitHub Secrets to store these values.

- Ensure islambda=true in the CLI command.

## Demo

https://github.com/pgupteqa/PythonSeleniumRobotFramework/blob/master/Video-Allure-passed-test-robot-framework.gif

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`INSTANCE_URL`

`SF_USERNAME`

`PASSWORD`

`SECURITY_TOKEN`

`CONSUMER_KEY`

`CONSUMER_SECRET`

`LT_USERNAME`

`LT_ACCESS_KEY`

