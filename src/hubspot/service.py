from pprint import pprint
import hubspot
from hubspot.crm.deals import ApiException as DealApiException
from hubspot.crm.companies import SimplePublicObjectInput as CompanySimplePublicObjectInput, ApiException as CompanyApiException
from hubspot.crm.owners import ApiException as OwnerApiException
from hubspot.crm.quotes import ApiException as QuoteApiException
from .config import Config


class HubspotService:

    def __init__(self, token: str):
        self.client: hubspot.Client = hubspot.Client.create(access_token=token)


    def get_deals(self, limit=100, after=None):
        try:
            api_response = self.client.crm.deals.basic_api.get_page(
                limit=limit,
                archived=False,
                after=after,
                properties=[
                    "estado_clickup",
                    "dealname",
                    "hubspot_owner_id",
                ]
            )
            return api_response.to_dict()
        except DealApiException as e:
            print("Exception when calling basic_api->get_page: %s\n" % e)


    def get_deal_associations(self, deal_id, to_object_type:str, limit=100):
        try:
            response = self.client.crm.deals.associations_api.get_all(
                deal_id=deal_id,
                limit=100,
                to_object_type=to_object_type
            )
            return response.to_dict()
        except DealApiException as e:
            print("Exception when calling AssociationsApi->get_all: %s\n" % e)
  

    def get_company(self, company_id):
        try:
            response = self.client.crm.companies.basic_api.get_by_id(
                company_id=company_id,
                properties=[
                    "name",
                    "phone",
                    "website",
                    "hubspot_owner_id",
                ]
            )
            return response.to_dict()
        except CompanyApiException as e:
            print("Exception when calling basic_api->get_by_id: %s\n" % e)
            return None


    def update_company(self, company_id, properties):

        simple_public_object_input = CompanySimplePublicObjectInput(properties=properties)

        try:
            response = self.client.crm.companies.basic_api.update(
                company_id=company_id,
                simple_public_object_input=simple_public_object_input
            )
            return response.to_dict()
        except CompanyApiException as e:
            print("Exception when calling basic_api->update: %s\n" % e)
            return None

    
    def get_owners(self, email:str=None, limit=100, after=None):
        try:
            response = self.client.crm.owners.owners_api.get_page(
                email=email,
                limit=limit,
                after=after
            )
            return response.to_dict()
            # return response.
        except OwnerApiException as e:
            print("Exception when calling OwnersApi->get_page: %s\n" % e)
            return None


    def get_quote_by_id(self, quote_id):
        try:
            response = self.client.crm.quotes.basic_api.get_by_id(
                quote_id=quote_id
            )
            return response.to_dict()
        except QuoteApiException as e:
            print("Exception when calling basic_api->get_by_id: %s\n" % e)
            return None


hubspot_client = HubspotService(Config.HUBSPOT_TOKEN)

      