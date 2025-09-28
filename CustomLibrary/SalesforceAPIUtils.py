import os
from pathlib import Path

from dotenv import load_dotenv
from robot.api.deco import library, keyword
from simple_salesforce import Salesforce, SalesforceAuthenticationFailed

@library
class SalesforceAPIUtils:

    def __init__(self):
        self.sf = self.authenticate_salesforce()

    @keyword
    def authenticate_salesforce(self):
        try:

            # Check if .env file exists, if yes load it, otherwise use Jenkins env vars
            project_root = Path(__file__).resolve().parents[1]
            env_path = project_root / ".env"
            if env_path.exists():
                print("Found .env file, loading environment variables from file...")
                load_dotenv(dotenv_path=env_path)
            else:
                print("No .env file found, using Jenkins environment variables...")

            sf_username = os.getenv("SF_USERNAME")
            sf_password = os.getenv("PASSWORD")
            sf_instance_url = os.getenv("INSTANCE_URL")
            sf_consumer_key = os.getenv("CONSUMER_KEY")
            sf_consumer_secret = os.getenv("CONSUMER_SECRET")

            if not all([sf_username, sf_password, sf_instance_url, sf_consumer_key, sf_consumer_secret]):
                raise ValueError("Missing Salesforce authentication configuration.")

            sf = Salesforce(username=sf_username,password=sf_password,instance_url=sf_instance_url,
                            consumer_key=sf_consumer_key,consumer_secret=sf_consumer_secret)
            return sf
        except SalesforceAuthenticationFailed as e:
            raise
        except Exception as ex:
            raise


    @keyword
    def get_lead_record_by_lastname(self, lastName, fields):

        try:
            fields_str = ','.join(fields)
            soql = f"SELECT {fields_str} from Lead where LastName='{lastName}'"
            responseresult = self.sf.query(soql)
            results = []
            if responseresult['totalSize'] > 0 and 'records' in responseresult:
                for record in responseresult['records']:
                    filtered_record = {field: record.get(field) for field in fields}
                    results.append(filtered_record)
                return results
            else:
                assert False, f"No Lead records found for LastName: {lastName}"

        except Exception as ex:
            raise

    @keyword
    def get_contact_record_by_lastname(self, lastName, fields):

        try:
            fields_str = ','.join(fields)
            soql = f"SELECT {fields_str} from Contact where LastName='{lastName}'"
            responseresult = self.sf.query(soql)
            results = []
            if responseresult['totalSize'] > 0 and 'records' in responseresult:
                for record in responseresult['records']:
                    filtered_record = {field: record.get(field) for field in fields}
                    results.append(filtered_record)
                return results
            else:
                assert False, f"No Lead records found for LastName: {lastName}"

        except Exception as ex:
            raise

    @keyword
    def get_account_record(self, contactId, fields):
        try:
            fields_str = ','.join(fields)
            soql = f"SELECT {fields_str} from Contact where Id='{contactId}'"
            responseresult = self.sf.query(soql)
            results = []
            if responseresult['totalSize'] > 0 and 'records' in responseresult:
                for record in responseresult['records']:
                    filtered_record = {field: record.get(field) for field in fields}
                    results.append(filtered_record)
                return results
            else:
                assert False, f"No Lead records found for LastName: {contactId}"

        except Exception as ex:
            raise

    @keyword
    def get_opportunity_record(self, contactId, fields):
        try:
            fields_str = ','.join(fields)
            soql = f"SELECT {fields_str} from Opportunity where ContactID='{contactId}'"
            responseresult = self.sf.query(soql)
            results = []
            if responseresult['totalSize'] > 0 and 'records' in responseresult:
                for record in responseresult['records']:
                    filtered_record = {field: record.get(field) for field in fields}
                    results.append(filtered_record)
                return results
            else:
                assert False, f"No Lead records found for LastName: {contactId}"

        except Exception as ex:
            raise

