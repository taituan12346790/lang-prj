import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import MetaData
from app.models.base import Base
import os
from dotenv import load_dotenv

load_dotenv()

async def create_tables():
    # Lấy DATABASE_URL từ environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ Lỗi: DATABASE_URL không được set trong .env")
        return
    
    print(f"🔌 Đang kết nối tới database...")
    engine = create_async_engine(database_url, echo=True)
    async with engine.begin() as conn:
        # Tạo tất cả bảng
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("✅ Đã tạo các bảng thành công!")

if __name__ == "__main__":
    asyncio.run(create_tables())