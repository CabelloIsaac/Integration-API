from pprint import pprint

import requests

import hubspot
from hubspot.crm.companies import ApiException as CompanyApiException
from hubspot.crm.companies import \
    SimplePublicObjectInput as CompanySimplePublicObjectInput
from hubspot.crm.deals import ApiException as DealApiException, SimplePublicObjectInput as DealSimplePublicObjectInput
from hubspot.crm.line_items import ApiException as LineItemApiException
from hubspot.crm.objects import ApiException as ObjectApiException
from hubspot.crm.objects import SimplePublicObjectInput
from hubspot.crm.owners import ApiException as OwnerApiException
from hubspot.crm.quotes import ApiException as QuoteApiException

from .config import Config
from .constants import Associations

from src.logging.service import LoggingService

logging_service = LoggingService(module="hubspot")

class HubspotService:

    def __init__(self, token: str):
        self.client: hubspot.Client = hubspot.Client.create(access_token=token)


    def get_association_specs(self, from_object_type:str, to_object_type:str):
        url = f"https://api.hubapi.com/crm/v4/associations/{from_object_type}/{to_object_type}/labels"

        headers = {
            'accept': "application/json",
            'authorization': "Bearer " + Config.HUBSPOT_TOKEN,
            }

        response = requests.request("GET", url, headers=headers)

        return response.json()["results"]


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
            logging_service.error("Exception when calling basic_api->get_page: %s\n" % e)


    def update_deal(self, deal_id, properties):
        try:
            simple_public_object_input = DealSimplePublicObjectInput(
                properties=properties
            )
            api_response = self.client.crm.deals.basic_api.update(
                deal_id=deal_id,
                simple_public_object_input=simple_public_object_input
            )
            return api_response.to_dict()
        except DealApiException as e:
            logging_service.error("Exception when calling basic_api->update: %s\n" % e)


    def get_deal_associations(self, deal_id, to_object_type:str, limit=100):
        try:
            response = self.client.crm.deals.associations_api.get_all(
                deal_id=deal_id,
                limit=100,
                to_object_type=to_object_type
            )
            return response.to_dict()
        except DealApiException as e:
            logging_service.error("Exception when calling AssociationsApi->get_all: %s\n" % e)
  

    def create_deal_association(self, deal_id, to_object_type:str, to_object_id:str):
        association_spec = self.get_association_specs(
            from_object_type=Associations.DEALS,
            to_object_type=to_object_type
        )

        if len(association_spec) == 0:
            logging_service.error (f"No se ha encontrado el tipo de asociación entre 'Deals' y '{to_object_type}'")
            return None

        association_spec_formatted = []

        for spec in association_spec:
            association_spec_formatted.append({
                "associationCategory": spec["category"],
                "associationTypeId": spec["typeId"]
            })

        try:
            response = self.client.crm.deals.associations_api.create(
                deal_id=deal_id,
                to_object_type=to_object_type,
                to_object_id=to_object_id,
                association_spec=association_spec_formatted
            )
            return response.to_dict()
        except DealApiException as e:
            logging_service.error("Exception when calling AssociationsApi->create: %s\n" % e)
            return None


    def create_custom_object_association(self, object_type:str, object_id:str, to_object_type:str, to_object_id:str):
        association_spec = self.get_association_specs(
            from_object_type=object_type,
            to_object_type=to_object_type
        )

        if len(association_spec) == 0:
            logging_service.error (f"No se ha encontrado el tipo de asociación entre '{object_type}' y '{to_object_type}'")
            return None

        try:
            api_response = self.client.crm.objects.associations_api.create(
                object_type=object_type,
                object_id=object_id,
                to_object_type=to_object_type,
                to_object_id=to_object_id,
                association_type=association_spec[0]["typeId"],
            )
            return api_response.to_dict()    
        except ObjectApiException as e:
            logging_service.error("Exception when calling associations_api->create: %s\n" % e)
            return None


    def get_company(self, company_id):
        try:
            response = self.client.crm.companies.basic_api.get_by_id(
                company_id=company_id,
                properties=[
                    "name",
                    "hubspot_owner_id",
                    "c_s__owner",
                    "description",
                    "nif_cif",
                ]
            )
            return response.to_dict()
        except CompanyApiException as e:
            logging_service.error("Exception when calling basic_api->get_by_id: %s\n" % e)
            return None


    def create_company_association(self, company_id, to_object_type:str, to_object_id:str):
        association_spec = self.get_association_specs(
            from_object_type=Associations.COMPANIES,
            to_object_type=to_object_type
        )

        if len(association_spec) == 0:
            logging_service.error (f"No se ha encontrado el tipo de asociación entre 'Companies' y '{to_object_type}'")
            return None

        association_spec_formatted = []

        for spec in association_spec:
            association_spec_formatted.append({
                "associationCategory": spec["category"],
                "associationTypeId": spec["typeId"]
            })

        try:
            response = self.client.crm.companies.associations_api.create(
                company_id=company_id,
                to_object_type=to_object_type,
                to_object_id=to_object_id,
                association_spec=association_spec_formatted
            )
            return response.to_dict()
        except CompanyApiException as e:
            logging_service.error("Exception when calling AssociationsApi->create: %s\n" % e)
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
            logging_service.error("Exception when calling basic_api->update: %s\n" % e)
            return None

    
    def get_owners(self, email:str=None, limit=100, after=None):
        try:
            response = self.client.crm.owners.owners_api.get_page(
                email=email,
                limit=limit,
                after=after
            )
            return response.to_dict()
        except OwnerApiException as e:
            logging_service.error("Exception when calling OwnersApi->get_page: %s\n" % e)
            return None


    def get_owner_by_id(self, owner_id):
        try:
            response = self.client.crm.owners.owners_api.get_by_id(
                owner_id=owner_id
            )
            return response.to_dict()
        except OwnerApiException as e:
            logging_service.error("Exception when calling OwnersApi->get_by_id: %s\n" % e)
            return None


    def get_quote_by_id(self, quote_id):
        try:
            response = self.client.crm.quotes.basic_api.get_by_id(
                quote_id=quote_id
            )
            return response.to_dict()
        except QuoteApiException as e:
            logging_service.error("Exception when calling basic_api->get_by_id: %s\n" % e)
            return None


    def get_quote_associations(self, quote_id, to_object_type:str, limit=100):
        try:
            response = self.client.crm.quotes.associations_api.get_all(
                quote_id=quote_id,
                limit=100,
                to_object_type=to_object_type
            )
            return response.to_dict()
        except QuoteApiException as e:
            logging_service.error("Exception when calling AssociationsApi->get_all: %s\n" % e)
            return None


    def get_line_item_by_id(self, line_item_id):
        try:
            response = self.client.crm.line_items.basic_api.get_by_id(
                line_item_id=line_item_id,
                properties=[
                    "name",
                    "hs_sku",
                ]
            )
            return response.to_dict()
        except LineItemApiException as e:
            logging_service.error("Exception when calling basic_api->get_by_id: %s\n" % e)
            return None


    def create_custom_object(self,object_type:str, properties):
        simple_public_object_input = SimplePublicObjectInput(properties=properties)

        try:
            response = self.client.crm.objects.basic_api.create(
                object_type=object_type,
                simple_public_object_input=simple_public_object_input
            )
            return response.to_dict()
        except ObjectApiException as e:
            logging_service.error("Exception when calling basic_api->create: %s\n" % e)
            return None


    def get_custom_objects(self, object_type, limit=100, after=None):
        try:
            response = self.client.crm.objects.basic_api.get_page(
                object_type=object_type,
                limit=limit,
                properties=["clickup_id"],
            )
            return response.to_dict()
        except ObjectApiException as e:
            logging_service.error("Exception when calling basic_api->get_page: %s\n" % e)
            return None


    def update_custom_object(self, object_type:str, object_id, properties):
        simple_public_object_input = SimplePublicObjectInput(properties=properties)

        try:
            response = self.client.crm.objects.basic_api.update(
                object_type=object_type,
                object_id=object_id,
                simple_public_object_input=simple_public_object_input
            )
            return response.to_dict()
        except ObjectApiException as e:
            logging_service.error("Exception when calling basic_api->update: %s\n" % e)
            return None


hubspot_client = HubspotService(Config.HUBSPOT_TOKEN)

      