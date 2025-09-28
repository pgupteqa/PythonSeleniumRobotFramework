import json
import os
from pathlib import Path

from dotenv import load_dotenv
from robot.api.deco import library, keyword
from robot.libraries.BuiltIn import BuiltIn



@library
class CommonUtility:


    @property
    def selenium(self):
        return BuiltIn().get_library_instance("BrowserUtilLibrary")

    def get_test_data_file_path(self, filename):
        HOME_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # print(HOME_dir)
        configfilepath = os.path.join(HOME_dir, 'TestData', filename)
        return  configfilepath


    @keyword
    def get_data_from_json(self, filename, keyname):
        path = self.get_test_data_file_path(filename)
        with open(path) as f:
            test_data = json.load(f)
            test_list = test_data[keyname]
            return test_list