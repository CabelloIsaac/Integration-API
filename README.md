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
uvicorn main:app --reload
```

## Endpoints

### POST /client

Create a new client.

#### Request

```json
{
        "name": "Test client",
        "description": "Test client description",
        "status": "inbox",
        "assignees": [3182376]
}
```
