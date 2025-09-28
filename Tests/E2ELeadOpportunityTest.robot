# Created by HP at 06-09-2025
*** Settings ***
Resource    ../Resources/Common.robot

Suite Setup      Run Keywords    Setup Lead E2E Test Data
Test Setup       Open SF Login Page
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
    Validate Created Opportunity    Prospecting

*** Keywords ***
Create Lead Record and Get Lead Lastname
    ${contactleadname}  Create new lead record    ${leadrecorddata}
    Set test variable    ${contactleadname}

