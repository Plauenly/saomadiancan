from fastapi import Request, HTTPException, Header, Depends
from datetime import datetime, timedelta, timezone
from asyncmy.cursors import DictCursor
import jwt

from config import settings

# 获取连接池
async def get_db_pool(request : Request):
    return request.app.state.db_pool

async def get_client_pool(request : Request):
    return request.app.state.client

# 包装sql请求, 返回字典
async def sql_fetch_one(pool, sql, args=None):
    async with pool.acquire() as conn:
        async with conn.cursor(DictCursor) as cur:
            await cur.execute(sql, args)
            return await cur.fetchone()

# 包装sql请求, 返回元组的字典
async def sql_fetch_all(pool, sql, args=None):
    async with pool.acquire() as conn:
        async with conn.cursor(DictCursor) as cur:
            await cur.execute(sql, args)
            return await cur.fetchall()


async def sql_execute(pool, sql, args=None):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            return await cur.execute(sql, args)

# 鉴权token相关
def create_token(user_id: int, openid: str):
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    payload = {
        "sub": str(user_id),
        "openid": openid,
        "exp": expire
    }
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.SIGN_ALGORITHM
    )
    return token

check_user_sql = "select id from user where open_id = %s and id = %s"

async def check_token(authorization: str = Header(), pool = Depends(get_db_pool)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未提供有效的认证凭证")
    # 用空格分割，取第二部分
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithm=[settings.SIGN_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token 已过期，请重新登录")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="认证失败，无效的 Token", headers={"WWW-Authenticate": "Bearer"},)

    openid = payload.get("openid")
    id = payload.get("id")
    res = await sql_fetch_one(pool, check_user_sql,  (payload.get("openid"), payload.get("id")))
    if res is not None:
        return {"openid":openid, "id":id}
    else:
        raise HTTPException(status_code=401, detail="认证失败，无效的 Token", headers={"WWW-Authenticate": "Bearer"},)