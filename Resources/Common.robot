# Created by HP at 27-08-2025
*** Settings ***
Library      ../CustomLibrary/SalesforceAPIUtils.py
Library      ../CustomLibrary/BrowserUtilLibrary.py
Library     ../PageObjects/LeadsPage.py
Library     ../PageObjects/LoginPage.py
Library     ../CustomLibrary/CommonUtilLibrary.py
Library    OperatingSystem

*** Variables ***
${Browser}
${headless}
${envname}
${islambda}

*** Keywords ***
Open SF Login Page
    Open browser with options     ${Browser}    ${headless}     ${envname}  ${islambda}
    Set selenium implicit wait    20s
    Set selenium page load timeout    20s

Close Browser Session
    Capture screenshot failure
    Close all browsers

Validate SF Authentication
    Authenticate salesforce

Go To Leads App
    Navigate To Leads App   ${envname}

Setup Lead E2E Test Data
   [Documentation]     This Keyword is used to setup Lead e2e testdata
   ${listuser}          Get Data From Json    loginTestData.json  valid_login
   Set suite variable   ${validusername}     ${listuser["username"]}
   ${validpassword}     Get Password From Env Val
   Set suite Variable    ${validpassword}

   ${leadrecorddata}=    Get Data from Json    leadOpportunityTestData.json    leadData
   Set suite variable    ${leadrecorddata}

Setup Login Test Data
    [Documentation]     This Keyword is used to setup valid login or invalid login testdata
    ${listuser}     Get Data from Json    loginTestData.json  valid_login
    Set suite variable   ${validusername}     ${listuser["username"]}
    ${validpassword}     Get Password From Env Val
    Set suite Variable    ${validpassword}

    ${invalidlistuser}  Get Data from Json    loginTestData.json  invalid_login
    Set suite variable   ${invalidusername}     ${invalidlistuser["username"]}
    Set suite variable   ${invalidpassword}     ${invalidlistuser["password"]}

Clean Allure Result Directory
    Run Keyword And Ignore Error    Remove Directory    allure-results   recursive=true
    # Recreate empty allure-result folder before running any tests
    Create Directory    allure-results






