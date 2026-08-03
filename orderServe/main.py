from fastapi import FastAPI
from fastapi import Request
from fastapi.staticfiles import StaticFiles
import uvicorn
import httpx
from db import init_db, close_db
from contextlib import asynccontextmanager
from router.login import login_api
from router.menu import menu_api
from router.order import order_api

# 用来在app运行前初始化连接池,app结束前关闭连接池。@asynccontextmanager 将该异步函数变为可以使用async with操作的对象
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(app)
    print("数据库连接池已创建")
    app.state.client = httpx.AsyncClient(timeout=15.0)
    print("https连接池已创建")
    yield

    await app.state.client.aclose()
    print("https连接池已关闭")
    await close_db(app)
    print("数据库连接池已关闭")
    


app = FastAPI(lifespan=lifespan)
app.include_router(login_api, prefix="/api/login", tags=["weixin login",])
app.include_router(menu_api, prefix="/api/menu", tags=["get menu",])
app.include_router(order_api, prefix="/api/orders", tags=["get or post order",])

if __name__ == '__main__':
    uvicorn.run("main:app",host="127.0.0.1",port=8080, reload=True)