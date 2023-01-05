from fastapi import FastAPI

from .click_up.router import router as clickup_router
from .hubspot.router import router as hubspot_router
from .router import router as root_router

app = FastAPI()

app.include_router(root_router)
app.include_router(clickup_router)
app.include_router(hubspot_router)
 