from aiogram.fsm.state import State, StatesGroup


class startSG(StatesGroup):
    start = State()
    sub_date = State()
    subscription = State()
    about = State()
    profile = State()
    card = State()
    confirm_card = State()
    crypto_choose = State()
    crypto = State()
    confirm_crypto = State()


class adminSG(StatesGroup):
    main = State()
    malling = State()
    get_mail = State()
    confirm_malling = State()
    sub_management = State()
    user_info = State()
    sub_change = State()

    