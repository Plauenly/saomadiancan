from fastapi import APIRouter, Header, Depends
from time import time
from typing import Dict
import json

import utils
from schema import Product1img, simOrder, comOrder, postOrder
from config import settings

order_api = APIRouter()

get_orders_sql = "SELECT * FROM orders WHERE open_id = %s;"
get_1order_sql = "SELECT * FROM orders WHERE open_id = %s and id = %s;"
get_product_sql = "SELECT p.* FROM product AS p INNER JOIN order_product AS op ON op.pid = p.id WHERE op.oid = %s;"
get_1imge_sql = "SELECT url FROM image_product WHERE pid = %s and sort = 0;"

get_num_sql = "SELECT num FROM num_log WHERE trans_date = %s"
#根据以上的num来更新与插入,并且作为一个完整的事务提交
update_num_sql = "UPDATE num_log SET num = %s WHERE trans_date = %s"
insert_num_sql = "INSERT INTO num_log (trans_date, num) VALUES (%s, %s)"

insert_orders_sql = "INSERT INTO orders (status, remark, open_id, phone, trade_id, total_price, create_at, shop_num) VALUES " \
                                    "(%(status)s,%(remark)s,%(open_id)s,%(phone)s,%(trade_id)s,%(total_price)s,%(create_at)s,%(shop_num)s);"
update_suorders_sql = "UPDATE orders SET status = %s ,pay_at = %s WHERE id = %s"
update_faorders_sql = "UPDATE orders SET status = %s WHERE id = %s"

@order_api.get("")
async def get_orders(user: Dict = Depends(utils.check_token), pool=Depends(utils.get_db_pool)):
    oresults = await utils.sql_fetch_all(pool, get_orders_sql, (user.get("openid"),))
    orders = []
    for ores in oresults:
        order = simOrder(**ores)
        commodity_list = []
        presults = await utils.sql_fetch_all(pool, get_product_sql, (ores.get("id"),))
        for pre in presults:
            product = Product1img(**pre)
            img = await utils.sql_fetch_one(pool, get_1imge_sql, (product.id))
            product.image = img.get("url")
            commodity_list.append(product)
        order.commodity_list = commodity_list
        orders.append(order)
    return orders

@order_api.get("/{oid}")
async def get_one_order(oid = int, user: Dict = Depends(utils.check_token), pool=Depends(utils.get_db_pool)):
    oresult = await utils.sql_fetch_one(pool, get_1order_sql, (user.get("openid"), oid))
    order = comOrder(**oresult)
    commodity_list = []
    presults = await utils.sql_fetch_all(pool, get_product_sql, (order.id,))
    for pre in presults:
        product = Product1img(**pre)
        img = await utils.sql_fetch_one(pool, get_1imge_sql, (product.id))
        product.image = img.get("url")
        commodity_list.append(product)
    order.commodity_list = commodity_list

    return order

@order_api.post("")
async def post_order(order:postOrder, 
                     user:Dict = Depends(utils.check_token), 
                     pool=Depends(utils.get_db_pool)
                     ):
    order.open_id = user.get("openid")
    if order.torder is None or order.trade_id is None:
        num = await utils.sql_getNextNum(pool, get_num_sql, update_num_sql, insert_num_sql)
        order.torder, order.trade_id = utils.get_trade_id(num)
    utils.sql_execute(pool, insert_orders_sql, order.model_dump())
    # 跳转到微信支付api,返回prepare_id给前端

    params = {
        "appid" : settings.WECHAT_APP_ID,
        "mchid" : settings.WECHAT_MECHANT_ID,
        "description" : "",         # 店名字+商品名字
        "out_trade_no" : order.trade_id,
        "time_expire" :  "",        # 用户能够完成该笔订单支付的最后时限
        "notify_url" : "",          # 商户接收支付成功回调通知的地址
        "support_fapiao" : False,   
        "amount" : {
            "total" : int(100*order.total_price),
            "currency" : "CNY"
        },
        "payer" : {
            "openid" : order.open_id
        },
        "detail" : None,            # 不知道这个字段是干什么，到底有什么用

    }
    ts = time.time()
    body = json.dumps(params, ensure_ascii=False, separators=(',', ':'))
    sig = f'POST\n/v3/pay/transactions/jsapi\n{ts}\n{settings.WECHAT_NONCE_STR}\n{str(params)}\n'
    req_token = utils.get_client_token(sig)

    headers = {
        "Authorization" : req_token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }



# 还需要实现轮询向微信查单（定时任务），再接受到utify还要结束该轮询
  

    

