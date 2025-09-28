import os
from datetime import datetime
from pathlib import Path

import allure
from SeleniumLibrary import SeleniumLibrary
from dotenv import load_dotenv
from robot.api.deco import library, keyword
from robot.libraries.BuiltIn import BuiltIn
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.remote.client_config import ClientConfig


@library
class BrowserUtilLibrary(SeleniumLibrary):

    @keyword
    def open_browser_with_options(self, browser, headless=False, envname=None, islambda=False):

        global driver
        if str(islambda).lower() == "true":
            # Build LambdaTest remote URL from environment variables
            project_root = Path(__file__).resolve().parents[1]
            env_path = project_root / ".env"
            if env_path.exists():
                print("Found .env file, loading environment variables from file...")
                load_dotenv(dotenv_path=env_path)
            else:
                print("No .env file found, using Jenkins environment variables...")

            lt_username = os.getenv('LT_USERNAME')
            lt_access_key = os.getenv('LT_ACCESS_KEY')

            test_name = BuiltIn().get_variable_value("${TEST NAME}")

            # Use ClientConfig for secure authentication
            hub_url = "https://hub.lambdatest.com/wd/hub"
            client_config = ClientConfig(remote_server_addr=hub_url,username=lt_username,password=lt_access_key)

            if not lt_username or not lt_access_key:
                raise ValueError(
                    "LT_USERNAME and LT_ACCESS_KEY environment variables must be set for LambdaTest execution")

            #remote_url = f"https://{lt_username}:{lt_access_key}@hub.lambdatest.com/wd/hub"

            # LambdaTest capabilities
            lt_options = {
                "build": "Robot Framework Tests",
                "name": test_name,
                "platformName": "Windows 11",
                "browserVersion": "latest",
                "w3c": True
            }

            if browser.lower() == "chrome":
                options = Options()
                if str(headless).lower() == "true":
                    options.add_argument("--headless=new")
                    options.add_argument("--disable-gpu")
                    options.add_argument("--window-size=1920,1080")
                options.set_capability("lt:options", lt_options)
                driver = webdriver.Remote(command_executor=hub_url, options=options, client_config=client_config)

            elif browser.lower() == "firefox":
                options = FirefoxOptions()
                if str(headless).lower() == "true":
                    options.add_argument("--headless")
                options.set_capability("lt:options", lt_options)
                driver = webdriver.Remote(command_executor=hub_url, options=options, client_config=client_config)

            elif browser.lower() == "edge":
                options = EdgeOptions()
                if str(headless).lower() == "true":
                    options.add_argument("--headless")
                options.set_capability("lt:options", lt_options)
                driver = webdriver.Remote(command_executor=hub_url, options=options, client_config=client_config)
        
        else:
            #chrome browser options

            if browser.lower() == "chrome":
                options = Options()
                if str(headless).lower() == "true":
                    options.add_argument("--headless=new")
                    options.add_argument("--disable-gpu")
                    options.add_argument("--window-size=1920,1080")

                driver = webdriver.Chrome(options=options)

            elif browser.lower() == "firefox":
                options = FirefoxOptions()
                if str(headless).lower() == "true":
                    options.add_argument("--headless")
                    options.add_argument("--disable-gpu")
                    options.add_argument("--window-size=1920,1080")

                driver = webdriver.Firefox(options=options)

            elif browser.lower() == "edge":
                options = EdgeOptions()
                if str(headless).lower() == "true":
                    options.add_argument("--headless")
                    options.add_argument("--disable-gpu")
                    options.add_argument("--window-size=1920,1080")

                driver = webdriver.Edge(options=options)

            else:
                raise ValueError(f"Unsupported browser: {browser}")

        # Register driver in SeleniumLibrary
        self.register_driver(driver, alias="SalesforceBrowser")

        url=self.get_org_env_url(envname)
        self.go_to(url)
        self.maximize_browser_window()

    @keyword
    def capture_screenshot_failure(self):
        """Capture screenshot in root/screenshots if test failed."""
        status = BuiltIn().get_variable_value("${TEST STATUS}")
        name = BuiltIn().get_variable_value("${TEST NAME}")

        if status == "FAIL":
            # always create screenshots folder in root
            folder = os.path.join(os.getcwd(), "screenshots")
            os.makedirs(folder, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = name.replace(" ", "_").replace(":", "_")
            file_path = os.path.join(folder, f"{safe_name}_{timestamp}.png")

            self.capture_page_screenshot(file_path)

            # Attach to Allure
            with open(file_path, "rb") as f:
                allure.attach(f.read(),name=f"Screenshot - {name}",attachment_type=allure.attachment_type.PNG)

            BuiltIn().log(f"Screenshot saved: {file_path}", console=True)



    def get_test_data_file_path(self, filename):
        HOME_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        configfilepath = os.path.join(HOME_dir, "TestData", filename)
        return configfilepath


    def get_data_from_json(self, filename, keyname):
        path = self.get_test_data_file_path(filename)
        with open(path) as f:
            test_data = json.load(f)
            return test_data[keyname]


    def get_org_env_url(self, keyname):
        env = self.get_data_from_json("salesforceOrgEnvDetails.json", keyname)
        return env["org_url"]