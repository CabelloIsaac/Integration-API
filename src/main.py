from fastapi import FastAPI

from .click_up.router import router as clickup_router

app = FastAPI()
app.include_router(clickup_router)
 