from routers import auth_route
import sys

from fastapi import FastAPI

print("System Path", sys.path)

app = FastAPI()

app.include_router(auth_route.router)
