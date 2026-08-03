from fastapi import APIRouter, Header, Depends
from typing import Dict

import utils
from schema import Product1img, simOrder, comOrder

order_api = APIRouter()

get_orders_sql = "SELECT * FROM orders WHERE open_id = %s"
get_1order_sql = "SELECT * FROM orders WHERE open_id = %s and id = %s"
get_product_sql = "SELECT p.* FROM product AS p INNER JOIN order_product AS op ON op.pid = p.id WHERE op.oid = %s"
get_1imge_sql = "SELECT url FROM image_product WHERE pid = %s and sort = 0"

@order_api.get("")
async def get_orders(user: Dict = Depends(utils.check_token), pool=Depends(utils.get_db_pool)):
    assert user is not None
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
    return order

@order_api.get("/{id}")
async def get_one_order(id = int, user: Dict = Depends(utils.check_token), pool=Depends(utils.get_db_pool)):
    assert user is not None
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