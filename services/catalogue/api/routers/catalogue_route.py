from fastapi import APIRouter

router = APIRouter(prefix="/catalogue", tags=["catalogue"])


@router.get("/")
def get_catalogue():
    # Return dummy catalogue
    return [{"sku_id": 1, "category_id": 1, "metadata_blob": "test"}]
