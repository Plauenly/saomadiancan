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
        async with conn.cursor(DictCursor) as cur:
            return await cur.execute(sql, args)

# 鉴权token相关
def create_token(user_id: int, openid: str):
    expire = datetime.now() + timedelta(days=7)
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

def get_trade_id(num:int):
    now = datetime.now().strftime()
    tar = str(num)
    tar = (5 -len(tar))*'0'+tar
    return "M"+tar, "znn_"+now+"_m"+tar

# sql事务处理
async def sql_getNextNum(pool, qsql, usql, isql, transdate=None):
    async with pool.acquire() as conn:
        await conn.autocommit(False)
        async with conn.cursor(DictCursor) as cur:
            try:
                await cur.execute(qsql, transdate)
                qres = await cur.fetchone()
                if qres is not None:
                    num = qres.get("num")+1
                    await cur.execute(usql, (num, transdate[0]))
                else :
                    num = 1
                    await cur.execute(isql, (transdate[0], num))
                conn.commit()
                return num
            except Exception as e:
                await conn.rollback()
                raise e
            finally:
                conn.autocommit(True)