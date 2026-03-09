from models.models import Transaction
from schemas.schemas import CreateTransaction
from sqlalchemy.ext.asyncio import AsyncSession




class TransactionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    
    async def create_transaction(self, data: CreateTransaction):
        transaction = Transaction(
            amount=data.amount,
            type=data.type,
            description=data.description,
            client_fk=data.client_fk
            
            
        )
        self.session.add(transaction)
        await self.session.flush()
        return transaction

    


    
        