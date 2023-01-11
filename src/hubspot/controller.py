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


def get_quote(quote_id):
    return hubspot_client.get_quote_by_id(quote_id=quote_id)


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


def get_projects():
    
    after = None
    is_last_page = False
    projects = []

    while not is_last_page:
        try:
            print (f"Getting projects after {after}")
            response = hubspot_client.get_custom_objects(
                object_type=Config.HUBSPOT_PROJECT_OBJECT_TYPE,
                after=after
            )
            projects.extend(response["results"])

            if response["paging"] is not None:
                after = response["paging"]["next"]["after"]
                print (after)
            else:
                print ("No more projects")
                is_last_page = True
                after = None

        except KeyError:
            print ("No more projects")
            after = None
            is_last_page = True
            break

    return projects


def set_deal_as_added_to_clickup(deal_id):
    print (f"Setting deal {deal_id} as added to ClickUp")
    return hubspot_client.update_deal(deal_id=deal_id, properties={"estado_clickup": EstadoClickup.ANADIDO_A_CLICKUP})


def get_company(company_id):
    return hubspot_client.get_company(company_id=company_id)


def get_owner_by_email(email):
    results = hubspot_client.get_owners(email=email)["results"]
    if len(results) > 0:
        return results[0]
    return None


def get_owner_by_id(owner_id):
    return hubspot_client.get_owner_by_id(owner_id=owner_id)


def pick_cs_owner_based_on_line_items(line_items_data: list):
    
    print ("\nPicking CS owner based on line items")
    
    line_item_skus = [line_item["sku"] for line_item in line_items_data]
    # line_item_skus.append("KD-RRSS")
    # line_item_skus.append("KD-WEB")
    # line_item_skus.append("KD-ECOM")
    
    print (f"Line item SKUs: {line_item_skus}")
    
    cs_owners_data = Config.CS_OWNERS_DATA
    
    if len(line_item_skus) == 1:
        # Se asigna al CS owner especialista en el producto
        print (f"Assigning to CS owner expert in product {line_item_skus[0]}")
        
        for cs_owner_data in cs_owners_data:
            if line_item_skus[0] in cs_owner_data["products"]:
                cs_owner_email = cs_owner_data["email"]
                break
    
    elif len(line_item_skus) % 2 == 0:
        # Se asigna a un CS owner de forma aleatoria
        print ("Assigning to random CS owner")
        
        random_cs_owner_data = random.choice(cs_owners_data)
        cs_owner_email = random_cs_owner_data["email"]
    
    elif len(line_item_skus) % 2 != 0:
        # Se asigna al CS Owner con más especialidades
        print ("Assigning to CS owner with more specialities")
        
        counters = {}
        for line_item_sku in line_item_skus:
            for cs_owner_data in cs_owners_data:
                if line_item_sku in cs_owner_data["products"]:
                    if cs_owner_data["email"] in counters:
                        counters[cs_owner_data["email"]] += 1
                    else:
                        counters[cs_owner_data["email"]] = 1
    
        print (f"Counters: {counters}")
        
        # Se obtiene el CS Owner con más especialidades
        for counter in counters:
            if counters[counter] == max(counters.values()):
                cs_owner_email = counter
                break
    
    cs_owner = get_owner_by_email(cs_owner_email)
    
    if cs_owner is None:
        print (f"CS Owner {cs_owner_email} not found")
        return None
    
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
        "clickup_project_status": project["clickup_project_status"],
    }
    print (f"Updating project {project_id}")
    print (properties)
    return hubspot_client.update_custom_object(object_type=Config.HUBSPOT_PROJECT_OBJECT_TYPE, object_id=project_id, properties=properties)


def set_click_up_status_in_project(click_up_status, click_up_id):
    print (f"Setting ClickUp status {click_up_status} in project {click_up_id}")
    properties = {
        "clickup_project_status": click_up_status,
    }
    
    projects = get_projects()
    for project in projects:
        if project["properties"]["clickup_id"] == click_up_id:
            project_id = project["id"]
            print (f"Updating project {project_id}")
            hubspot_client.update_custom_object(object_type=Config.HUBSPOT_PROJECT_OBJECT_TYPE, object_id=project_id, properties=properties)


def assign_cs_owner_to_company(company, line_items_data: list[dict]):

    company_id = company["id"]
    
    cs_owner_id = pick_cs_owner_based_on_line_items(line_items_data=line_items_data)
    

    if company is not None:
        current_company_owner_id = company["properties"]["c_s__owner"]
        if current_company_owner_id is None or current_company_owner_id == "":

            cs_owner_id = pick_cs_owner_based_on_line_items(line_items_data=line_items_data)

            print (f"Assigning company owner: {cs_owner_id}")
            properties = {"c_s__owner": cs_owner_id}
            company = hubspot_client.update_company(company_id=company_id, properties=properties)
            print (f"New company owner: {company['properties']['c_s__owner']}")
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

            # If company does not have nif_cif, skip it
            if company["properties"]["nif_cif"] is None or company["properties"]["nif_cif"] == "":
                print ("Company has no nif_cif. Skipping...")
                continue

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

            # If quote is DRAFT, skip it
            quote = get_quote(quote_id=quote_id)
            if quote["properties"]["hs_status"] == "DRAFT":
                print (f"Quote '{quote_id}' is DRAFT. Skipping...")
                continue

            line_items_data = []

            # Loop through quote line_items
            for quote_line_item in quote_line_items:
                line_item_id = quote_line_item["to_object_id"]
                line_item = get_line_item_by_id(line_item_id=line_item_id)
                line_item_sku = line_item["properties"]["hs_sku"]
                line_item_name = line_item["properties"]["name"]
                # print (line_item)
                line_items_data.append({
                    "id": line_item_id,
                    "sku": line_item_sku,
                    "name": line_item_name,
                })

            print (f"Line items skus: {line_items_data}")

            # Update Deal single_line_products_list field
            single_line_products_list = Utils.build_single_line_products_list(line_items_data=line_items_data)
            print (f"single_line_products_list: {single_line_products_list}")
            properties = {
                "single_line_products_list": single_line_products_list,
            }
            deal = hubspot_client.update_deal(deal_id=deal_id, properties=properties)
            
            
            # Assign CS Owner to COMPANY based on line_items
            company = assign_cs_owner_to_company(company=company, line_items_data=line_items_data)
            return company

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
            for line_item_data in line_items_data:
                line_item_id = line_item_data["id"]
                line_item_data = line_item_data["sku"]

                project_name = Utils.build_project_name(sku=line_item_data, deal_name=deal_name)

                project = create_project(project_name=project_name)
                if project is None:
                    print ("Project not created. Skipping...")
                    continue

                print (f"\nProject created: {line_item_data} - {project['id']}")
                project_id = project["id"]

                products.append({
                    "id": project_id,
                    "sku": line_item_data,
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

    owner_id = company["properties"]["c_s__owner"]
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