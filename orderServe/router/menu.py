from fastapi import APIRouter,Depends

import utils
import schema

get_category_sql = "SELECT * FROM category"
get_product_sql = "SELECT p.* FROM product AS p INNER JOIN category_product AS cp ON cp.pid = p.id WHERE cp.cid = %s"
get_image_sql = "SELECT * FROM image_product WHERE pid = %s"
get_label_sql = "SELECT l.* FROM label AS l INNER JOIN label_product AS lp ON lp.lid = l.id WHERE lp.pid = %s"

menu_api = APIRouter()

def keep_hnum(num : int):
    if num == 0 or num < 10:
        return num
    s = str(num)
    return int(s[0] + '0' * (len(s) - 1))
    
@menu_api.get("")
async def get_menu(db_pool=Depends(utils.get_db_pool)):
    categorys = []
    cresults = await utils.sql_fetch_all(db_pool, get_category_sql)
    for cres in cresults:
        products = []
        cid = cres.get("id")
        presults = await utils.sql_fetch_all(db_pool, get_product_sql, (cid,))
        for pres in presults:
            images = []
            labels = []
            pid = pres.get("id")
            iresults = await utils.sql_fetch_all(db_pool, get_image_sql, (pid,))
            for ires in iresults:
                images.append(schema.Image(**ires))
            lresults = await utils.sql_fetch_all(db_pool, get_label_sql, (pid,))
            for lres in lresults:
                labels.append(schema.Label(**ires))
            product = schema.Product(**pres)
            product.images = images
            product.labels = labels
            product.sold = keep_hnum(product.sold)
            product.category_id = cid
            products.append(product)
        category = schema.Category(**cres)
        category.products = products
        categorys.append(category)
    return categorys
