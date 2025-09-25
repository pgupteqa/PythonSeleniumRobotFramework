# Created by HP at 27-08-2025
*** Settings ***
Library      ../CustomLibrary/BrowserUtilLibrary.py
Library      ../CustomLibrary/SalesforceAPIUtils.py
Library     ../PageObjects/LeadsPage.py
Library     ../PageObjects/LoginPage.py
Library     ../CustomLibrary/CommonUtilLibrary.py
Resource    ./Variables.robot

*** Keywords ***
Open Login Page
    Open browser    url=${url}  browser=${Browser}
    Maximize browser window
    Set selenium implicit wait    20s
    Set selenium page load timeout    20s

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
   ${listuser}     Get Data from Json    loginTestData.json  valid_login
   Set suite variable   ${validusername}     ${listuser["username"]}
   Set suite variable   ${validpassword}     ${listuser["password"]}

   ${leadrecorddata}=    Get Data from Json    leadOpportunityTestData.json    leadData
   Set suite variable    ${leadrecorddata}

Setup Login Test Data
    [Documentation]     This Keyword is used to setup valid login or invalid login testdata
    ${listuser}     Get Data from Json    loginTestData.json  valid_login
    Set suite variable   ${validusername}     ${listuser["username"]}
    Set suite variable   ${validpassword}     ${listuser["password"]}

    ${invalidlistuser}     Get Data from Json    loginTestData.json  invalid_login
    Set suite variable   ${invalidusername}     ${invalidlistuser["username"]}
    Set suite variable   ${invalidpassword}     ${invalidlistuser["password"]}




