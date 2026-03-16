from schemas.schemas import CreateTransaction
from repositories.transaction_repository import TransactionRepository
from database.unit_of_work import UnitOfWork
from models.models import Transaction
from fastapi import HTTPException, status





class TransactionService:



    @staticmethod
    async def create_transaction(data: CreateTransaction) -> Transaction:
        async with UnitOfWork() as uow:
            transaction = await uow.transaction.create_transaction(data)
            if not transaction:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            return transaction


    @staticmethod
    async def get_transaction(transaction_id: int) -> Transaction:
        async with UnitOfWork() as uow:
            transactions = await uow.transaction.get_transaction(transaction_id)

            if not transactions:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found.")
            
            total = sum(t.amount for t in transactions)


            result = []


            return result.append({
                "transaction_id": transactions,
                "total": total
            })
        