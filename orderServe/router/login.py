from datetime import datetime, timezone
from fastapi import APIRouter, Request, HTTPException, Depends

import db
import utils
from config import settings
# from schema import User

login_api = APIRouter()

wx_login_url = "https://api.weixin.qq.com/sns/jscode2session"

find_user_sql = "SELECT * FROM USER WHERE open_id = %s;"
insert_user_sql = "INSERT INTO USER (open_id, create_at, last_login) VALUES(%s,%s,%s);"
update_user_sql = "UPDATE USER SET last_login = %s WHERE open_id = %s;"

# id, open_id 


# prefix = "/api/login"
@login_api.post("")
async def login(req : Request, client=Depends(utils.get_client_pool), db_pool=Depends(utils.get_db_pool)):

    data = await req.json()
    code = data.get("code")
    params = {
        "appid": settings.WECHAT_APP_ID,
        "secret": settings.WECHAT_APP_SECRET,
        "js_code": code,
        "grant_type": "authorization_code"
    }
    #应该要设置请求头吧
    response = await client.get(wx_login_url, params=params, timeout=10)

    result = response.json()
    if "errcode" in result :
        if result["errcode"] == -1 or result["errcode"] == 45011:
            raise HTTPException(status_code=503, detail=f"微信系统繁忙，请稍候重试: {result.get('errmsg')}")
        if result["errcode"] == 40029:
            raise HTTPException(status_code=400, detail=f"请求的数据已过期，请重试: {result.get('errmsg')}")
        if result["errcode"] == 40226:
            raise HTTPException(status_code=400, detail=f"高风险用户，不能使用微信小程序: {result.get('errmsg')}")
    openid = result.get("openid")
    if not openid:
        raise HTTPException(status_code=400, detail="获取openid失败")
    # session_key = result.get("session_key")

    sql_response = await utils.sql_fetch_one(db_pool, find_user_sql, (openid,))
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if sql_response is None:
        await utils.sql_execute(db_pool, insert_user_sql, {"open_id":openid, "create_at":now, "last_login":now})
        sql_response = await utils.sql_fetch_one(db_pool, find_user_sql, (openid,))
    else:
        await utils.sql_execute(db_pool, update_user_sql, {"open_id":openid, "last_login":now})

    user_id = sql_response.get("id")
    token = utils.create_token(user_id, openid)
    print(token)
    return {"token": token}


    

