from fastapi import FastAPI
import time

app = FastAPI()


# GET
@app.get("/")
def get_catalog():
    # Return dummy catalog
    return [{"sku_id": 1, "category_id": 1, "metadata_blob": "test"}]

# POST
