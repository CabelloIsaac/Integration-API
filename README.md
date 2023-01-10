# Integration API

API to integrate with ClickUp, HubSpot and more.

## Setup

1. Install the requirements

```bash
pip install -r requirements.txt
```

2. Create a `.env` file with the following content:

```bash
# CLICKUP
CLICKUP_ACCESS_TOKEN = ""
CLICKUP_TEAM_ID = ""
CLICKUP_CLIENTES_SPACE_ID = ""
CLICKUP_CLIENTES_FOLDER_ID = ""
CLICKUP_CLIENTES_LIST_ID = ""

CLICKUP_PRODUCTOS_FOLDER_ID = ""
```

3. Run the script

```bash
uvicorn src.main:app --reload
```

## Main Endpoints

### GET /sync/clients

Take the Deals from HubSpot with the "estado_clickup" property set to "Listo" and create the corresponding tasks and projects in ClickUp.

How it works:

#### HubSpot

1. Get the deals from HubSpot with the "estado_clickup" property set to "Listo"
2. For each deal:
   1. Get the Quote associated with the deal
   2. Create a Contract and link it to the Deal and the Company
   3. Create the Projects in the Quote and link them to the Contract and Company
   4. Send the data to the ClickUp module.

#### ClickUp

   1. Create the Client in ClickUp
   2. Create the Products in ClickUp and link them to the Client
   3. Returns the Products created in ClickUp to HubSpot

#### HubSpot

   1. Add the Products ids, url and status to the corresponding Project in HubSpot
   2. Update the "estado_clickup" property of the Deal to "Añaadido a ClickUp"

## Test Endpoints

### POST /clickup/client

Create a new client. A client is a task in the list `Clientes` in the folder `Clientes` in the space `Clientes`.
The id of the list, folder and space are defined in the config.py file of the clickup module.

Also:

- The task is created in the status `inbox`.
- The task is assigned to the `cs_owner` sent in the request.
- Creates the products as new tasks
- Links the products to the client task

#### Request

```json
{
  "name": "Test.com",
  "description": "Online tests and testing for certification, practice tests, test making tools, medical testing and more.",
  "nif_cif": "12345678A",
  "cs_owner": "desarrollo.isaac@alotofpipol.com",
  "send_slack_notification": true,
  "send_email_notification": true,
  "products": [
    {
      "id": 3131923132,
      "sku": "KD-ECOM"
    },
    {
      "id": 3131923133,
      "sku": "KD-RRSS"
    }
  ],
  "custom_fields": [
    {
      "name": "ID_CLIENTE_HUBSPOT",
      "value": "6753679830"
    }
  ]
}
```

### GET /clickup/task/sync-all

Sync all the subtasks's custom fields with the parent task's custom fields.
The tasks proccessed are the ones in the PRODUCTOS folder.
The PRODUCTOS folder is defined in the `.env` file.

### POST /clickup/task/sync

Sync the subtasks's custom fields with the parent task's custom fields.
The task to sync is the one sent in the request.
Also:
  Updates the task status on the corresponding Project in HubSpot.

#### Request

```json
{
  "task_id": "PROD-871", // This can be the task id or the task custom id
  "custom_task_ids": true // Set to true if the task_id is a custom id
}
```

#### Response

```json
{
  "status": "ok",
  "updated_task": {
    "id": "3xxwt0r",
    "name": "KD-WEB: CORREDURIA DE SEGUROS LOPEZ BONMATI SL",
    "url": "https://app.clickup.com/t/3xxwt0r"
  },
  "updated_subtasks": [
    {
      "id": "865bcmd2d",
      "name": "hola",
      "url": "https://app.clickup.com/t/865bcmd2d"
    },
    {
      "id": "3xxwt3f",
      "name": "WEB-12: C.S. Presentaciu00f3n a Cliente web funcional v1",
      "url": "https://app.clickup.com/t/3xxwt3f"
    },
  ]
}
```

### GET /hubspot/deals

Get all the deals from HubSpot.

### GET /hubspot/deals/process

Process the deals from HubSpot.
Get all the deals from HubSpot with the "estado_clickup" property set to "Listo" and create the corresponding Contract and Projects
in the Quote associated with the deal.