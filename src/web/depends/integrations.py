from src.integrations.users import UsersClient


async def get_users_client() -> UsersClient:
    return UsersClient()
