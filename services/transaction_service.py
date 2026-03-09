from schemas.schemas import CreateTransaction
from repositories.transaction_repository import TransactionRepository
from unit_of_work import UnitOfWork
from models.models import Transaction
from fastapi import HTTPException, status
from typing import List




class TransactionService:



    @staticmethod
    async def create_transaction(data: CreateTransaction) -> Transaction:
        async with UnitOfWork() as uow:
            transaction = await uow.transaction.create_transaction(data)
            if not transaction:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            return transaction






        