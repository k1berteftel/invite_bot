from aiogram.fsm.state import State, StatesGroup


class startSG(StatesGroup):
    start = State()
    sub_date = State()
    subscription = State()
    about = State()
    card = State()
    crypto = State()


class adminSG(StatesGroup):
    main = State()
    malling = State()
    get_mail = State()
    confirm_malling = State()
    