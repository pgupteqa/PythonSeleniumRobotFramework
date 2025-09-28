from robot.api.deco import library, keyword
from robot.libraries.BuiltIn import BuiltIn

from BasePage import BasePage

@library
class LeadsPage(BasePage):

    #Locators for Leads Page
    LEADS_TAB_LOCATOR = "xpath://span[@class='slds-truncate'][normalize-space()='Leads']"
    NEW_LEAD_BUTTON_LOCATOR = "xpath://li[@data-target-selection-name='sfdc:StandardButton.Lead.New']"
    LEAD_SALUTATION = "xpath://button[@aria-label='Salutation']"
    LEAD_SALUTATION_PICKIST = "xpath://div[@aria-label='Salutation']//lightning-base-combobox-item"
    LEAD_FIRSTNAME_LOCATOR = "xpath://input[@name='firstName']"
    LEAD_LASTNAME_LOCATOR = "xpath://input[@name='lastName']"
    LEAD_COMPANY_NAME_LOCATOR = "xpath://input[@name='Company']"
    LEAD_EMAIL_LOCATOR = "xpath://input[@name='Email']"
    SAVE_BUTTON = "xpath://button[@name='SaveEdit']"
    LEAD_SUCCESS_MESSAGE_LOCATOR = "xpath://div[contains(@class,'slds-theme--success forceToastMessage')]"

    LEAD_CONVERTED_BUTTON_LOCATOR2 = "xpath://li[@data-name='converted']/a[@aria-selected='false']"
    LEAD_CONVERTED_BUTTON_LOCATOR = "xpath://a[@aria-selected='false']//span[@class='title slds-path__title'][normalize-space()='Converted']"
    LEAD_MARK_STATUS_COMPLETE_BUTTON_LOCATOR = "xpath://button[.='Select Converted Status']"
    LEAD_CONVERT_BUTTON_LOCATOR = "xpath://button[.='Convert']"
    LEAD_CONVERT_SUCCESS_MESSAGE_LOCATOR = "xpath://div[@class='title']/h2"
    GOTO_LEAD_BUTTON = "xpath://button[.='Go to Leads']"


    @keyword
    def navigate_to_leads_app(self,envname):
        orgbaseurl = self.get_base_org_url(envname)
        lead_url = orgbaseurl + f"lightning/o/Lead/list?filterName=__Recent"
        self.selenium.go_to(lead_url)
        self.wait_for_visibility_of_element(self.NEW_LEAD_BUTTON_LOCATOR)
        title = self.selenium.get_title()
        assert "Leads" in title

    @keyword
    def create_new_lead_record(self, lead_data_json):

        self._click_new_lead_button()
        self._fill_new_lead_data(lead_data_json)
        self._click_save_button()
        return self._get_generated_lastname()

    '''private helpers methods for lead creation'''
    def _click_new_lead_button(self):
        self.selenium.click_element(self.NEW_LEAD_BUTTON_LOCATOR)
        self.wait_for_visibility_of_element(self.LEAD_SALUTATION)

    '''add new lead private helper method to add mandatory data'''
    def _fill_new_lead_data(self,lead_data_json):
        self.wait_for_visibility_of_element(self.LEAD_SALUTATION)
        self.selenium.click_element(self.LEAD_SALUTATION)

        self.wait_for_visibility_of_element(self.LEAD_SALUTATION_PICKIST)
        self.select_option_from_picklist(self.LEAD_SALUTATION_PICKIST, "Mr.")

        self.wait_for_visibility_of_element(self.LEAD_FIRSTNAME_LOCATOR)
        self.selenium.input_text(self.LEAD_FIRSTNAME_LOCATOR, lead_data_json["firstname"])

        self.wait_for_visibility_of_element(self.LEAD_LASTNAME_LOCATOR)
        self.generated_lastname = self.random_string()
        self.selenium.input_text(self.LEAD_LASTNAME_LOCATOR, self.generated_lastname)

        self.wait_for_visibility_of_element(self.LEAD_COMPANY_NAME_LOCATOR)
        self.get_account_name = lead_data_json["company"] + self.random_string()
        self.selenium.input_text(self.LEAD_COMPANY_NAME_LOCATOR, self.get_account_name)

        self.wait_for_visibility_of_element(self.LEAD_EMAIL_LOCATOR)
        self.getlead_email = "testautomation" + self.generated_lastname + "@mailinator.com"
        self.selenium.input_text(self.LEAD_EMAIL_LOCATOR, self.getlead_email)

    def _click_save_button(self):
        self.selenium.click_element(self.SAVE_BUTTON)

    def _get_generated_lastname(self):
        """Return the generated lastname for use in subsequent tests"""
        return getattr(self, 'generated_lastname', None)



    @keyword
    def validate_lead_status_should_be(self, status):
        LEAD_STATUS_TAB = f"xpath://a[@data-tab-name='{status}']"
        self.selenium.element_attribute_value_should_be(LEAD_STATUS_TAB,"aria-selected","true")

    @keyword
    def convert_lead(self):
        self.wait_for_visibility_of_element(self.LEAD_CONVERTED_BUTTON_LOCATOR)
        self.selenium.mouse_over(self.LEAD_CONVERTED_BUTTON_LOCATOR)
        self.selenium.press_keys(self.LEAD_CONVERTED_BUTTON_LOCATOR2, "ENTER")
        self.wait_for_visibility_of_element(self.LEAD_MARK_STATUS_COMPLETE_BUTTON_LOCATOR)
        self.selenium.press_keys(self.LEAD_MARK_STATUS_COMPLETE_BUTTON_LOCATOR, "ENTER")
        self.wait_for_visibility_of_element(self.LEAD_CONVERT_BUTTON_LOCATOR)
        self.selenium.mouse_over(self.LEAD_CONVERT_BUTTON_LOCATOR)
        self.selenium.press_keys(self.LEAD_CONVERT_BUTTON_LOCATOR, "ENTER")
        self.wait_for_visibility_of_element(self.LEAD_CONVERT_SUCCESS_MESSAGE_LOCATOR)
        leadconvertmsg = self.selenium.get_text(self.LEAD_CONVERT_SUCCESS_MESSAGE_LOCATOR)
        assert "Your lead has been converted" in leadconvertmsg

    @keyword
    def validate_created_contact_record(self, lastname):
        self.selenium.mouse_over(self.GOTO_LEAD_BUTTON)
        self.selenium.click_element(self.GOTO_LEAD_BUTTON)
        fields = ["Id", "Name", "Email"]
        contactdetails = self.sf_authenticate.get_contact_record_by_lastname(lastname, fields)
        for data in contactdetails:
            self.contactnameval = data["Name"]
            self.contactid = data["Id"]
            self.contact_email = data["Email"]

        assert lastname in self.contactnameval

    @keyword
    def validate_created_account(self):
        fields = ["Id", "Name"]
        contactdetails = self.sf_authenticate.get_account_record(self.contactid, fields)
        for data in contactdetails:
            self.accountname = data["Name"]
            self.accountId = data["Id"]

        #assert self.get_account_name ==  self.accountname
        BuiltIn().should_be_equal(self.get_account_name,self.accountname)

    @keyword
    def validate_created_opportunity(self,stageval):
        fields = ["Id", "Name", "StageName"]
        contactdetails = self.sf_authenticate.get_opportunity_record(self.contactid, fields)
        for data in contactdetails:
            self.opp_name = data["Name"]
            self.opp_Id = data["Id"]
            self.opp_stage = data["StageName"]

        # assert self.get_account_name ==  self.accountname
        BuiltIn().should_be_equal(stageval, self.opp_stage)

    @keyword
    def navigate_to_contact_after_lead_conversion(self, envname):
        self.navigate_to_contact_page(self.contactid, self.contactnameval,envname)



        













