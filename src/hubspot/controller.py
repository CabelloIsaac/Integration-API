import random

from .utils import Utils
from .service import hubspot_client
from .constants import EstadoClickup, Associations
from .config import Config
from ..constants import ClickUpCustomFields


def get_deal_companies(deal_id):
    return hubspot_client.get_deal_associations(deal_id=deal_id, to_object_type=Associations.COMPANIES)["results"]


def get_deal_quotes(deal_id):
    return hubspot_client.get_deal_associations(deal_id=deal_id, to_object_type=Associations.QUOTES)["results"]


def associate_contract_with_deal(deal_id, contract_id):
    print (f"Associating deal {deal_id} with contract {contract_id}")
    return hubspot_client.create_deal_association(deal_id=deal_id, to_object_type=Associations.CONTRACTS, to_object_id=contract_id)


def associate_contract_with_company(company_id, contract_id):
    print (f"Associating company {company_id} with contract {contract_id}")
    return hubspot_client.create_company_association(company_id=company_id, to_object_type=Associations.CONTRACTS, to_object_id=contract_id)


def associate_project_with_company(company_id, project_id):
    print (f"Associating company {company_id} with project {project_id}")
    return hubspot_client.create_company_association(company_id=company_id, to_object_type=Associations.PROJECTS, to_object_id=project_id)


def associate_project_with_contract(contract_id, project_id):
    print (f"Associating contract {contract_id} with project {project_id}")
    return hubspot_client.create_custom_object_association(
        object_type=Associations.CONTRACTS,
        object_id=contract_id,
        to_object_type=Associations.PROJECTS,
        to_object_id=project_id
    )


def get_quote_line_items(quote_id):
    return hubspot_client.get_quote_associations(quote_id=quote_id, to_object_type=Associations.LINE_ITEMS)["results"]


def get_line_item_by_id(line_item_id):
    return hubspot_client.get_line_item_by_id(line_item_id=line_item_id)


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


def set_deal_as_added_to_clickup(deal_id):
    print (f"Setting deal {deal_id} as added to ClickUp")
    return hubspot_client.update_deal(deal_id=deal_id, properties={"estado_clickup": EstadoClickup.ANADIDO_A_CLICKUP})


def get_company(company_id):
    return hubspot_client.get_company(company_id=company_id)


def get_owner_by_email(email):
    return hubspot_client.get_owners(email=email)["results"][0]


def get_owner_by_id(owner_id):
    return hubspot_client.get_owner_by_id(owner_id=owner_id)


def get_random_cs_owner():
    cs_owner_email = random.choice(Config.CS_OWNERS_EMAILS)
    cs_owner = get_owner_by_email(cs_owner_email)
    cs_owner_id = cs_owner["id"]

    print (f"Got {cs_owner_email} ({cs_owner_id})")
    return cs_owner_id


def create_contract(contract_name):
    properties = {
        "contract_name": contract_name,
    }
    contract = hubspot_client.create_custom_object(object_type=Config.HUBSPOT_CONTRACT_OBJECT_TYPE,properties=properties)
    return contract
    

def create_project(project_name):
    properties = {
        "project_name": project_name,
    }
    project = hubspot_client.create_custom_object(object_type=Config.HUBSPOT_PROJECT_OBJECT_TYPE,properties=properties)
    return project


def update_project(project):
    project_id = project["hubspot_id"]
    properties = {
        "clickup_id": project["clickup_id"],
        "clickup_link": project["clickup_link"],
    }
    print (f"Updating project {project_id}")
    print (properties)
    return hubspot_client.update_custom_object(object_type=Config.HUBSPOT_PROJECT_OBJECT_TYPE, object_id=project_id, properties=properties)


def assign_cs_owner_to_company(company):

    company_id = company["id"]

    if company is not None:
        current_company_owner_id = company["properties"]["hubspot_owner_id"]
        if current_company_owner_id == "":

            cs_owner_id = get_random_cs_owner()

            print (f"Assigning company owner: {cs_owner_id}")
            properties = {"hubspot_owner_id": cs_owner_id}
            company = hubspot_client.update_company(company_id=company_id, properties=properties)
            print (f"New company owner: {company['properties']['hubspot_owner_id']}")
        else:
            print (f"Company {company['properties']['name']} already has an owner: {current_company_owner_id}")
        return company
    else:
        print ("Company not found")
        return None


def process_deals():

    deals = get_deals()
    click_up_clients = []

    # Loop through deals
    for deal in deals:
        deal_id = deal["id"]
        deal_name = deal["properties"]["dealname"]
        deal_status = deal["properties"]["estado_clickup"]

        # Check if deal is ready to be processed
        if deal_status == EstadoClickup.LISTO:
            print ("\n###############################################")
            print (f"Deal {deal_name} ({deal_id}) is ready to be processed")
            print (f"ClickUp Status: {deal_status}")

            company = None

            # Get deal's companies
            deal_companies = get_deal_companies(deal_id)
    
            # If deal has no company, skip it
            if len(deal_companies) == 0:
                print ("Deal has no company. Skipping...")
                continue
                
            company_id = deal_companies[0]["to_object_id"]
            company = get_company(company_id=company_id)

            # If company is not found, skip it
            if company is None:
                print ("Company not found. Skipping...")
                continue
            
            company = assign_cs_owner_to_company(company=company)

            deal_quotes = get_deal_quotes(deal_id)

            # If deal has no quotes, skip it
            if len(deal_quotes) == 0:
                print (f"Deal '{deal_name}' ({deal_id}) has no quotes")
                continue

            quote_id = deal_quotes[0]["to_object_id"]
            print (f"Deal '{deal_name}' ({deal_id}) has a quote: {quote_id}")

            quote_line_items = get_quote_line_items(quote_id=quote_id)
            
            # If quote has no line_items, skip it
            if len(quote_line_items) == 0:
                print (f"Quote '{quote_id}' has no line_items")
                continue

            line_items_skus = []

            # Loop through quote line_items
            for quote_line_item in quote_line_items:
                line_item_id = quote_line_item["to_object_id"]
                line_item = get_line_item_by_id(line_item_id=line_item_id)
                line_item_sku = line_item["properties"]["hs_sku"]
                line_items_skus.append({
                    "id": line_item_id,
                    "sku": line_item_sku
                })

            print (f"Line items skus: {line_items_skus}")

            # Create CONTRACT and link to COMPANY and DEAL
            contract = create_contract(contract_name=f"Contrato {deal_name}")
            if contract is None:
                print ("Contract not created. Skipping...")
                continue

            print (f"Contract created: {contract['id']}")
            contract_id = contract["id"]
        
            # Update DEAL with CONTRACT
            associate_contract_with_deal(deal_id=deal_id, contract_id=contract_id)

            # Update COMPANY with CONTRACT
            associate_contract_with_company(company_id=company_id, contract_id=contract_id)

            products = []

            # Create PROJECT for every line_item and link to COMPANY and CONTRACT
            for line_item_sku in line_items_skus:
                line_item_id = line_item_sku["id"]
                line_item_sku = line_item_sku["sku"]

                project_name = Utils.build_project_name(sku=line_item_sku, deal_name=deal_name)

                project = create_project(project_name=project_name)
                if project is None:
                    print ("Project not created. Skipping...")
                    continue

                print (f"\nProject created: {line_item_sku} - {project['id']}")
                project_id = project["id"]

                products.append({
                    "id": project_id,
                    "sku": line_item_sku,
                })

                # Update COMPANY with PROJECT
                associate_project_with_company(company_id=company_id, project_id=project_id)

                # Update CONTRACT with PROJECT
                associate_project_with_contract(contract_id=contract_id, project_id=project_id)

            print (f"\nBuilding ClickUp payload...")
            click_up_payload = build_click_up_payload(company=company, products=products, deal_id=deal_id)
            click_up_clients.append(click_up_payload)
        

    return click_up_clients


def build_click_up_payload(company, products, deal_id):

    owner_id = company["properties"]["hubspot_owner_id"]
    owner = get_owner_by_id(owner_id=owner_id)
    owner_email = owner["email"]
    enlace_hubspot = build_enlace_hubspot(company_id=company['id'])

    click_up_payload = {
        "name": company['properties']['name'],
        "description": company['properties']['description'],
        "nif_cif": company['properties']['nif_cif'],
        "cs_owner": owner_email,
        "hubspot_deal_id": deal_id,
        "products": products,
        "custom_fields": [
            {
                "name": ClickUpCustomFields.ID_CLIENTE_HUBSPOT,
                "value": company['id']
            },
            {
                "name": ClickUpCustomFields.ENLACE_HUBSPOT,
                "value": enlace_hubspot
            }
        ]
    }

    return click_up_payload


def build_enlace_hubspot(company_id):
    hubspot_user_id = Config.HUBSPOT_USER_ID
    return f"https://app.hubspot.com/contacts/{hubspot_user_id}/company/{company_id}"