from fastapi import FastAPI
from routers import catalogue_route

app = FastAPI()


app.include_router(catalogue_route.router)
