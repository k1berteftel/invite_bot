import datetime
from sqlalchemy import select, insert, update, column
from sqlalchemy.ext.asyncio import AsyncSession

from database.model import UsersTable

class DataInteraction():
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_user(self, user_id: int) -> None:
        stmt = insert(UsersTable).values(
            user_id=user_id,
            entry=datetime.datetime.today()
        )
        conf_stmt = stmt.on_conflict_do_nothing(index_elements=['telegram_id'])
        await self._session.execute(stmt)
        await self._session.commit()

    async def add_sub(self, user_id: int, sub_date: datetime.datetime) -> None:
        stmt = update(UsersTable).where(UsersTable.c.user_id == user_id).values(sub_date=sub_date)
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_sub_date(self, user_id: int) -> datetime.datetime:
        stmt = select(column('sub_date')).where(UsersTable.c.user_id == user_id).select_from(UsersTable)
        result = await self._session.execute(stmt)
        result = result.fetchmany(1)
        return result[0][0]