import random
from .service import hubspot_client
from .constants import EstadoClickup, Associations
from .config import Config


def get_deal_companies(deal_id):
    return hubspot_client.get_deal_associations(deal_id=deal_id, to_object_type=Associations.COMPANIES)


def get_deal_quotes(deal_id):
    return hubspot_client.get_deal_associations(deal_id=deal_id, to_object_type=Associations.QUOTES)


def get_deals():
    
    after = None
    is_last_page = False
    deals = []

    while not is_last_page:
        try:
            print (f"Getting deals after {after}")
            response = hubspot_client.get_deals(after=after)
            deals.extend(response["results"])

            if response["paging"] is not None:
                after = response["paging"]["next"]["after"]
                print (after)
            else:
                print ("No more deals")
                is_last_page = True
                after = None

        except KeyError:
            print ("No more deals")
            after = None
            is_last_page = True
            break

    return deals


def get_company(company_id):
    return hubspot_client.get_company(company_id=company_id)


def assign_cs_owner_to_company(company_id):

    cs_owner_email = random.choice(Config.CS_OWNERS_EMAILS)
    cs_owner = hubspot_client.get_owners(email=cs_owner_email)["results"][0]
    cs_owner_id = cs_owner["id"]

    print (f"Assigning {cs_owner_email} ({cs_owner_id}) to company {company_id}")

    company = get_company(company_id)

    if company is not None:
        current_company_owner_id = company["properties"]["hubspot_owner_id"]
        print (f"Current owner: {current_company_owner_id}")
        if current_company_owner_id == "":
            print ("Assigning new owner")
            properties = {"hubspot_owner_id": cs_owner_id}
            company = hubspot_client.update_company(company_id=company_id, properties=properties)
            print (f"New owner: {company['properties']['hubspot_owner_id']}")
        else:
            print (f"Company already has an owner: {current_company_owner_id}")
        return company
    else:
        print ("Company not found")
        return None


def process_deals():

    deals = get_deals()

    for deal in deals:
        deal_id = deal["id"]
        deal_name = deal["properties"]["dealname"]
        deal_status = deal["properties"]["estado_clickup"]
        deal_owner_id = deal["properties"]["hubspot_owner_id"]

        if deal_status == EstadoClickup.LISTO:
            print (f"Deal {deal_name} ({deal_id}) is ready to be processed")
            print (f"ClickUp Status: {deal_status}")
            print (f"Owner: {deal_owner_id}")

            company = None

            deal_companies = get_deal_companies(deal_id)
            if deal_companies != []:
                deal_companies = deal_companies["results"]
                company_id = deal_companies[0]["to_object_id"]
                assign_cs_owner_to_company(company_id=company_id)
            else:
                deal_companies = []

            if company is not None:
                print (f"Company: {company['properties']['name']}")