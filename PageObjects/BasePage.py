import random
import string
from pathlib import Path

from dotenv import load_dotenv
from robot.api.deco import library
from robot.libraries.BuiltIn import BuiltIn
from selenium.common import NoSuchElementException


@library
class BasePage:

    @property
    def selenium(self):
        #Selenium library used as Inheritance in browserlibrary class
        #so have used the browserUtilityLibrary as instance of selenium library
        return BuiltIn().get_library_instance("BrowserUtilLibrary")


    @property
    def sf_authenticate(self):
        return BuiltIn().get_library_instance("SalesforceAPIUtils")


    def select_option_from_picklist(self, locator, picklistvalue):
        self.selenium.wait_until_element_is_visible(locator, timeout='20s')
        picklist_options = self.selenium.get_webelements(locator)
        #for txt in picklist_options:
        #    print(txt.text)
        found = False
        for option in picklist_options:
           if option.text.strip() == picklistvalue:
                option.click()
                found = True
                break
        assert found, f"Picklist option '{picklistvalue}' is not found in the options"

    def random_string(self,size=6, chars=string.ascii_letters):
        """This method is use to generate random string data for name or other text"""
        return ''.join(random.choice(chars) for _ in range(size))

    def get_base_org_url(self,keyname):
        env = self.selenium.get_data_from_json("salesforceOrgEnvDetails.json", keyname)
        return env["lightning_view_url"]

    def click_using_javascript(self,locator):
        # Next try: JS click
        try:
            self.selenium.execute_javascript("arguments[0].click();", locator)
            return
        except Exception:
            pass

    def navigate_to_contact_page(self, contact_id, contact_name,envname):
        orgbase_url = self.get_base_org_url(envname)
        contact_url = orgbase_url + f"lightning/r/Contact/{contact_id}/view"
        self.selenium.go_to(contact_url)
        self.selenium.wait_until_page_contains(contact_name, timeout='20s')
        title = self.selenium.get_title()
        assert "Contact" in title

    def wait_for_visibility_of_element(self, locator):
        self.selenium.wait_until_element_is_visible(locator,timeout='20s')


    def enter_text_field(self, locator, value):
        """Helper method to enter text in form fields"""
        self.wait_for_visibility_of_element(locator)
        self.selenium.input_text(locator, value)