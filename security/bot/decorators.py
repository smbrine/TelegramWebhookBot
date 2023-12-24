from functools import wraps
from typing import Callable, List, Any


class BotSecurity:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(BotSecurity, cls).__new__(cls)
        return cls._instance

    def __init__(self, allowed_users: List[int]):
        if not hasattr(
            self, "initialized"
        ):  # Check if it's the first time initializing
            self.allowed_users = allowed_users
            self.initialized = True  # Ensure that __init__ doesn't reinitialize

    def is_allowed(self, f: Callable) -> Callable:
        @wraps(f)
        async def wrapper(*args, **kwargs) -> Any:
            user_id = args[1]["message"]["from"]["id"]
            if user_id in self.allowed_users:
                return await f(*args, **kwargs)
            else:
                return None

        return wrapper

    async def add_allowed_user(self, user_id: int):
        self.allowed_users.append(user_id)
        print(self.allowed_users)
