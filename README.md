# test-clickup-api

This is a test project to test the ClickUp API.

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
```

3. Run the script

```bash
uvicorn src.main:app --reload
```

## Endpoints

### POST /client

Create a new client. A client is a task in the list `Clientes` in the folder `Clientes` in the space `Clientes`.
The id of the list, folder and space are defined in the `.env` file.

Also:

- The task is created in the status `inbox`.
- The task is assigned to the `cs_owner` sent in the request.
- Creates the products as new tasks
- Links the products to the client task

#### Request

```json
{
  "name": "Test client",
  "description": "Test client description",
  "cif_nif": "12345678B",
  "cs_owner": "desarrollo.isaac@alotofpipol.com",
  "send_slack_notification": true,
  "send_email_notification": true,
  "products": [
    "KD-WEB"
  ],
  "custom_fields": [
    {
      "name": "¿SUBVENCIÓN APROBADA?",
      "value": "SÍ"
    },
    {
      "name": "ENLACE HUBSPOT",
      "value": "https://www.google.com/?hl=es"
    }
  ]
}
```

