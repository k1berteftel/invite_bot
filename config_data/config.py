from dataclasses import dataclass
from environs import Env


@dataclass
class tg_bot:
    token: str
    admin_ids: list[int]

@dataclass
class database:
    dns: str


@dataclass
class Config:
    bot: tg_bot
    db: database


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        bot=tg_bot(
            token=env('token'),
            admin_ids=list(map(int, env.list('admins')))
            ),
        db=database(
            dns=env('dns')
        )
        )
