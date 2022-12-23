
from fastapi import FastAPI
from routers.clickup import spaces_router, teams_router, lists_router,clickup_router

import sys, threading
# sys.setrecursionlimit(10**7) # max depth of recursion
# threading.stack_size(2**27)  # new thread will get stack of such size

app = FastAPI()
app.include_router(teams_router.router)
app.include_router(spaces_router.router)
app.include_router(lists_router.router)
app.include_router(clickup_router.router)
