import os
from pathlib import Path

from dotenv import load_dotenv
from robot.api.deco import library, keyword
from BasePage import BasePage


@library
class LoginPage(BasePage):

    # Locators for Salesforce Login
    USERNAME_FIELD = "id=username"
    PASSWORD_FIELD = "id=password"
    LOGIN_BUTTON = "id=Login"
    ERROR_MESSAGE = "id=error"
    REMEMBER_ME = "id=rememberUn"
    FORGOT_PASSWORD = "id=forgot_password_link"

    # Lightning Experience locators
    APP_LAUNCHER = "xpath://button[@title='App Launcher']"
    USER_PROFILE = "css=.profileTrigger"
    LOGOUT_LINK = "css=a[href*='logout']"
    LOGIN_ERROR = "id=error"

    @keyword
    def login_to_salesforce(self, username, password):

        self.selenium.wait_until_element_is_visible(self.USERNAME_FIELD)
        self.selenium.input_text(self.USERNAME_FIELD, username)

        self.selenium.wait_until_element_is_visible(self.PASSWORD_FIELD)
        self.selenium.input_password(self.PASSWORD_FIELD, password)

        self.selenium.click_button(self.LOGIN_BUTTON)

    @keyword
    def validate_app_launcher_icon(self):
        self.selenium.wait_until_element_is_visible(self.APP_LAUNCHER)
        self.selenium.page_should_contain_element(self.APP_LAUNCHER)

    @keyword
    def validate_login_error_message(self, expected_error_substring):
        self.selenium.page_should_contain_element(self.LOGIN_ERROR)
        actual_error_msg = self.selenium.get_text(self.LOGIN_ERROR)
        assert expected_error_substring in actual_error_msg

    @keyword
    def validate_lead_record_by_lastname(self,lstname):
        fields = ["Id", "Name", "Status"]
        leaddetails = self.sf_authenticate.get_lead_record_by_lastname(lstname,fields)
        for leaddata in leaddetails:
            self.leadnameval = leaddata["Name"]
            self.lead_idval = leaddata["Id"]

        print(f"this is record DETAIL:{self.leadnameval}")
        assert lstname in self.leadnameval

    @keyword
    def get_password_from_env_val(self):
        project_root = Path(__file__).resolve().parents[1]
        env_path = project_root / ".env"
        if env_path.exists():
            print("Found .env file, loading environment variables from file...")
            load_dotenv(dotenv_path=env_path)
            user_password = os.getenv("PASSWORD")
        else:
            print("No .env file found, using Jenkins environment variables...")
            user_password = os.environ.get("PASSWORD")

        return user_password