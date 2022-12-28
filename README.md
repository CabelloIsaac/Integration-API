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

CLICKUP_PRODUCTOS_FOLDER_ID = ""
```

3. Run the script

```bash
uvicorn src.main:app --reload
```

## Endpoints

### POST /clickup/client

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

### GET /clickup/task/sync-all

Sync all the subtasks's custom fields with the parent task's custom fields.
The tasks proccessed are the ones in the PRODUCTOS folder.
The PRODUCTOS folder is defined in the `.env` file.

### POST /clickup/task/sync

Sync the subtasks's custom fields with the parent task's custom fields.
The task to sync is the one sent in the request.

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