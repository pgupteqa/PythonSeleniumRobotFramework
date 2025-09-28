*** Settings ***
Resource    ../Resources/Common.robot

Suite Setup      Run Keywords   Setup Login Test Data
Test Setup       Open SF Login Page
Test Teardown    Close Browser Session
Test Tags       smoke   regression  logintest  test:retry(2)

*** Test Cases ***
Validate Valid Login
    [Documentation]     This is a valid login test
    [Tags]      validlogin
    Login to salesforce     username=${validusername}     password=${validpassword}
    Validate app launcher icon
    Validate lead record by lastname    FSLeadQA

Validate Invalid Login
    [Documentation]     This is a invalid login test
    [Tags]      invalidlogin
    Login to salesforce     username=${invalidusername}     password=${invalidpassword}
    Validate login error message    Please check your username and password
