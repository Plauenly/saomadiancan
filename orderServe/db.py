import asyncmy
from config import settings
# 连接池作为全局变量可被调用。
# 注意引用时候不要使用from db import pool,这样的pool是None。正确是import db 用db.pool来调用

async def init_db(app):
    app.state.db_pool = await asyncmy.create_pool(
        host=settings.DATABASE_URL,
        port=3306,
        user=settings.DATABASE_USERNAME,
        password=settings.DATABASE_PASSWORD,
        db=settings.DATABASE_NAME,
        minsize=5,
        maxsize=20,
        autocommit=True,
    )

async def close_db(app):
    app.state.db_pool.close()
    await app.state.db_pool.wait_closed()


