from schemas.schemas import OrderCreate
from models.models import Order
from fastapi import HTTPException, status
from database.unit_of_work import UnitOfWork


class OrderService:

        
    @staticmethod
    async def create_order(data: OrderCreate) -> Order:
        async with UnitOfWork() as uow:
            return await uow.order.create_order(data)
    

    @staticmethod
    async def get_orders(skip: int, limit: int) -> Order:
        async with UnitOfWork() as uow:
            order = await uow.order.get_order(skip, limit)
            if not order:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
            return order


    @staticmethod
    async def get_order(order_id: int) -> Order:
        async with UnitOfWork() as uow:
            order = await uow.order.get_order(order_id)
            if not order:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
            return order
    

    @staticmethod
    async def order_update(order_id: int, title: str) -> Order:
        async with UnitOfWork() as uow:
            order = await uow.order.get_order(order_id)
            if not order:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
            await uow.order.orders_update(order, title=title)
            return order
        

    async def add_product_to_order(self, order_id: int, product_id: int) -> Order:
        async with UnitOfWork() as uow:
            order = await uow.order.get_order(order_id)
            product = await uow.product.get_product(product_id)
            if not product or not order:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found products or order.")
            if product in order.products:
                raise HTTPException(status_code=status.HTTP_200_OK, detail="Product already in order.!")
            order.products.append(product)
            return order.products

    
    async def compeleted_order(self, order_id: int) -> Order:
        async with UnitOfWork() as uow:
            order = await uow.order.get_order(order_id)
            if order is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
            if order.status == "compeleted":
                raise HTTPException(status_code=status.HTTP_200_OK, detail="200.")
            order.status = "compeleted"
            return order
            
      

    @staticmethod
    async def order_client_sum(order_id: int) -> dict:
        async with UnitOfWork() as uow:
            order = await uow.order.get_order_selectionload(order_id)
            if not order:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
            total_price = sum(products.price for products in order.products)
            return {
                "order_id": order.id,
                "total_price": total_price
            }
        
        
    @staticmethod
    async def update_order_status(order_id: int, Status: str) -> Order:
        async with UnitOfWork() as uow:
            order = await uow.order.get_order(order_id)
            if not order:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
            return await uow.order.update_order_status(order, Status)
    
    @staticmethod
    async def create_order_client(client_id: int, product_id: int, title: str) -> Order:
        async with UnitOfWork() as uow:
            client = await uow.client.get_client(client_id)
            if not client:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found.")
            product = await uow.product.get_product(product_id)
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
            order = OrderCreate(
                title=title,
                client_id=client_id
            )
            order = await uow.order.create_order(order)
            # print(f"{order.products} p1")
            order.products.append(product)
            return order


    
    async def delete_product_from_order(self, order_id: int, product_id: int) -> Order:
        async with UnitOfWork() as uow:
            order = await uow.order.get_order(order_id)
            product = await uow.product.get_product(product_id)
            if not order:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
            if product not in order.products:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found product in orders.")
            order.products.remove(product)
            return order
            
    

    async def get_order_with_products(self, order_id: int) -> dict:
        async with UnitOfWork() as uow:
            order_with_products = await uow.order.get_order_selectionload(order_id)
            if not order_with_products:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="We can't find, order with products.")
            return {
                "order_with_products": order_with_products
            }
                






    