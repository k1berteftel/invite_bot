import datetime

from dateutil.relativedelta import relativedelta
from sqlalchemy import select, insert, update, column, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from database.model import UsersTable


class DataInteraction():

    def __init__(self, session: async_sessionmaker):
        self._sessions = session

    async def test_database(self) -> None:
        async with self._sessions() as session:
            await session.execute(text('SELECT 1'))

    async def check_user(self, user_id) -> bool:
        async with self._sessions() as session:
            result = await session.scalar(select(UsersTable).where(UsersTable.user_id == user_id))
        print(result)
        return True if result else False

    async def check_sub(self, user_id) -> datetime.datetime | bool:
        async with self._sessions() as session:
            result = await session.scalar(
                select(UsersTable.subscription).where(UsersTable.user_id == user_id).where(
                    UsersTable.subscription > datetime.datetime.today()).select_from(UsersTable))
        return result if result else False

    async def add_user(self, user_id: int, name: str, username: str) -> None:
        if await self.check_user(user_id):
            return
        stmt = insert(UsersTable).values(
            username=username,
            name=name,
            user_id=user_id,
            entry=datetime.datetime.today()
        )
        #  conf_stmt = stmt.on_conflict_do_nothing(index_elements=['telegram_id'])
        async with self._sessions() as session:
            await session.execute(stmt)
            await session.commit()

    async def add_sub(self, user_id: int, months: int | None) -> None:
        sub: datetime = await self.check_sub(user_id)
        print(sub)
        if months is None:
            stmt = update(UsersTable).where(UsersTable.user_id == user_id).values(
                subscription=None)
        elif sub:
            stmt = update(UsersTable).where(UsersTable.user_id == user_id).values(
                subscription=sub + relativedelta(months=months)
            )

            await self.add_extension(user_id)
        else:
            stmt = update(UsersTable).where(UsersTable.user_id == user_id).values(
                subscription=datetime.datetime.today() + relativedelta(months=months))
        async with self._sessions() as session:
            await session.execute(stmt)
            await session.commit()

    async def add_sub_days(self, user_id: int, days: int):
        async with self._sessions() as session:
            await session.execute(update(UsersTable).where(UsersTable.user_id == user_id).values(
                subscription=(await self.check_sub(user_id)) + relativedelta(days=days)
            ))
            await session.commit()

    async def add_extension(self, user_id: int):
        if await self.check_sub(user_id):
            async with self._sessions() as session:
                await session.execute(
                    update(UsersTable).where(UsersTable.user_id == user_id).values(extension=UsersTable.extension + 1))
                await session.commit()

    async def get_sub_date(self, user_id: int) -> datetime.datetime | bool:
        if not await self.check_sub(user_id):
            return False
        stmt = select(column('subscription')).where(UsersTable.user_id == user_id).select_from(UsersTable)
        async with self._sessions() as session:
            result = await session.scalar(stmt)
        return result

    async def get_active_subscriptions(self) -> int:
        async with self._sessions() as session:
            result = await session.scalars(
                select(UsersTable.user_id).where(UsersTable.subscription > datetime.datetime.today()).select_from(
                    UsersTable))
        print(result)
        return len(result.fetchall())

    async def get_subscriptions(self):
        async with self._sessions() as session:
            result = await session.scalars(
                select(UsersTable).where(UsersTable.subscription > datetime.datetime.today()).select_from(
                    UsersTable))
        print(result)
        return result.fetchall()

    async def get_new_users(self) -> int:
        async with self._sessions() as session:
            result = await session.scalars(
                select(UsersTable.user_id).where(UsersTable.entry > datetime.datetime.today() - relativedelta(months=1)))
        return len(result.fetchall())

    async def get_extensions(self) -> int:
        async with self._sessions() as session:
            result = await session.scalars(select(UsersTable.user_id).where(UsersTable.extension >= 1).select_from(UsersTable))
        return len(result.fetchall())

    async def get_users(self) -> any:
        async with self._sessions() as session:
            result = await session.scalars(select(UsersTable.user_id).select_from(UsersTable))
        return result.fetchall()

    async def get_user(self, user_id: int) -> UsersTable | bool:
        async with self._sessions() as session:
            result = await session.scalar(select(UsersTable).where(UsersTable.user_id == user_id).select_from(UsersTable))
        return result if result else False

    async def get_base(self) -> any:
        async with self._sessions() as session:
            result = await session.scalars(select(UsersTable))
        return result.fetchall()

    async def set_extension(self, user_id: int):
        async with self._sessions() as session:
            await session.execute(update(UsersTable).where(UsersTable.user_id == user_id).values(
                extension=0
            ))
            await session.commit()
