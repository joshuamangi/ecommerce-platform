from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from data.database import get_db

from handlers.order_handler import OrderHandler

from schema.order_schema import (
    OrderBase,
    OrderOut
)

router = APIRouter(
    prefix="/api/orders",
    tags=["orders"]
)


# GET ALL
@router.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def get_orders(
    db: AsyncSession = Depends(get_db)
):

    return await OrderHandler.fetch_all_orders(db=db)


# GET BY ID
@router.get(
    "/{order_id}",
    status_code=status.HTTP_200_OK,
    response_model=OrderOut
)
async def get_order_by_id(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):

    existing_order = await OrderHandler.fetch_order_by_id(
        db=db,
        order_id=order_id
    )

    if not existing_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return existing_order


# CREATE
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=OrderBase
)
async def create_order(
    order: OrderBase,
    db: AsyncSession = Depends(get_db)
):

    new_order = await OrderHandler.create_order(
        db=db,
        order=order
    )

    if not new_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Catalogue item not found"
        )

    return new_order


# UPDATE
@router.put(
    "/{order_id}",
    status_code=status.HTTP_200_OK,
    response_model=OrderOut
)
async def update_order(
    order_id: int,
    updated_order: OrderBase,
    db: AsyncSession = Depends(get_db)
):

    existing_order = await OrderHandler.update_order(
        db=db,
        order_id=order_id,
        updated_order=updated_order
    )

    if not existing_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return existing_order


# DELETE
@router.delete(
    "/{order_id}",
    status_code=status.HTTP_200_OK
)
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):

    existing_order = await OrderHandler.delete_order(
        db=db,
        order_id=order_id
    )

    if not existing_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return {
        "message": "Order deleted successfully"
    }
