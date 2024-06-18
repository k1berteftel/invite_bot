from handlers.user_handlers import user_router
from handlers.join_handlers import join_router

def get_handlers():
    return [user_router, join_router]