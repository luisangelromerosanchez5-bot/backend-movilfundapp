import asyncio
from app.core.database import get_supabase
from app.routers.auth import login
from app.schemas.auth import UserLogin

async def main():
    credentials = UserLogin(email="juan.gonzalez@fundapp.org", password="123")
    try:
        response = await login(credentials)
        print("SUCCESS:", response)
    except Exception as e:
        print("EXCEPTION:", e)

    credentials2 = UserLogin(email="juan.gonzalez@fundapp.org", password="12345678")
    try:
        response2 = await login(credentials2)
        print("SUCCESS:", response2)
    except Exception as e:
        print("EXCEPTION2:", e)

if __name__ == "__main__":
    asyncio.run(main())
