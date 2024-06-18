from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


class PostgresBuild:
    def __init__(self, dns: str):
        self.engine = create_async_engine(dns, echo=True)

    def session(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(self.engine, expire_on_commit=False)