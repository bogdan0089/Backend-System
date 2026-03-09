from schemas.schemas import ClientCreate, ClientUpdate, OrderCreate
from models.models  import Client
from fastapi import HTTPException, status
from typing import List
from unit_of_work import UnitOfWork


class ClientService:


    @staticmethod
    async def create_client(data: ClientCreate) -> Client:
        async with UnitOfWork() as uow:

            db_client = await uow.client.create_client(data)
            order_data = OrderCreate(
                title=f" Order for -> {db_client.id}",
                client_id=db_client.id
            )
            await uow.order.create_order(order_data)
            return db_client
    

    @staticmethod
    async def get_all_client() -> List[Client]:
        async with UnitOfWork() as uow:
            client = await uow.client.get_all_clients()
            if not client:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
            return client
    

    @staticmethod
    async def get_client(client_id: int) -> Client:
        async with UnitOfWork() as uow:
            client = await uow.client.get_client(client_id)
            if not client:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
            return client
    

    @staticmethod
    async def client_update(client_id: int, data: ClientUpdate) -> Client:
        async with UnitOfWork() as uow:
            db_client = await uow.client.get_client(client_id)
            if not db_client:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
            await uow.client.client_update(db_client, data)
            return db_client


    @staticmethod
    async def client_delete(client_id: int) -> Client:
        async with UnitOfWork() as uow:
            client = await uow.client.get_client(client_id)
            if not client:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
            orders = await uow.order.get_by_client_id(client_id)
            if orders:
                return {
                    "massage": "You can not delete client with active order!",
                    "count_order": len(client.orders)
                }
            if not client.orders:
                await uow.client.client_delete(client)
                return client



    @staticmethod
    async def get_client_order_count(client_id: int) -> dict:
        async with UnitOfWork() as uow:
            client = await uow.client.client_with_orders(client_id)
            if not client:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
            total_order = len(client.orders)
            return {
                "client_id": client_id,
                "orders_count": total_order
            }
        
        
    @staticmethod
    async def client_deposit(client_id: int, amount: float) -> Client:
        async with UnitOfWork() as uow:
                client = await uow.client.get_client(client_id)
                if not client:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found.")
                if amount <= 0:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount must be positive.")
                return await uow.client.deposit_client(client, amount)
    
        
    @staticmethod
    async def client_withdraw(client_id: int, amount: float) -> Client:
        async with UnitOfWork() as uow:        
            client = await uow.client.get_client(client_id)
            if not client:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found.")
            if amount > client.balance:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough money.")
            if amount <= 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount must be positive.")
            return await uow.client.withdraw_client(client, amount)


    


    

