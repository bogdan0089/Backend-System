from schemas.schemas import ProductsCreate, ProductsRead
from repositories.product_repository import ProductRepository
from models.models   import Product
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from unit_of_work import UnitOfWork


class ProductService:



    @staticmethod
    async def create_product(data: ProductsCreate) -> Product:
        async with UnitOfWork() as uow:
            return await uow.product.create_product(data)


    @staticmethod
    async def get_product(product_id: int) -> Product:
        async with UnitOfWork() as uow:
            products = await uow.product.get_product(product_id)
            if not products:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
            return products
        


