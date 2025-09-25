*** Settings ***
Resource    ../Resources/Common.robot

Test Setup    Run Keywords  Open SF Login Page  Setup Login Test Data
Test Teardown    Close Browser Session
Test Tags       smoke   regression  validlogin  test:retry(2)

*** Test Cases ***
Valid Login Test
    [Documentation]     This is a valid login test
    Login to salesforce     username=${validusername}     password=${validpassword}
    Validate app launcher icon
    Validate lead record by lastname    FSLeadQA

Invalid Login Test
    [Documentation]     This is a valid login test
    Login to salesforce     username=${invalidusername}     password=${invalidpassword}
    Validate login error message    Please check your username and password
