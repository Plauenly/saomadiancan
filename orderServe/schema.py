from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal
from datetime import datetime,timezone

import utils

class Image(BaseModel):
    url : str = ""

class Label(BaseModel):
    id : int
    name : str
    color : str = ""

class Product(BaseModel):
    id : int
    category_id : int
    name : str
    description : str = ""
    images : List[Image] = []
    labels : List[Label] = []
    price : Decimal = Decimal("0.00")
    status : int = 1
    sold : int 
    is_single : int = 1
    is_takeout : int = 1
    materials : List[int] = []

class Category(BaseModel):
    id : int 
    name : str
    category_image_url : str = ""
    products : List[Product] = []

class Product1img(BaseModel):
    id : int  = Field(exclude=True)                     #在返回时被忽略
    image : str = ""
    name : str = ""
    price : Decimal = Decimal("0.00")
    number : int = Field(default=0, alias="quantity")   #alias的作用是注入的时候只能用"quantity"属性，输出的时候只能用"number"

class simOrder(BaseModel):
    id : int
    # is_takeout : int = 0  #应该在每件商品里选择打包，而不是在订单里面选择打包
    # `is_takeout` tinyint(1) NOT NULL DEFAULT '0' COMMENT "方式: 0堂食, 1打包"
    # `is_refund` tinyint(1) NOT NULL DEFAULT '0' COMMENT "方式: 0 未退款, 1 已退款"
    status : int = 0
    shop_num : int = 0
    price : Decimal = Field(default=Decimal("0.00"), alias="total_price") 
    commodity_list: List[Product] = []

class comOrder(BaseModel):
    id : int
    torder : str
    status : int = 0
    shop_num : int = 0
    price : Decimal = Field(default=Decimal("0.00"), alias="total_price") 
    remark : str = ""
    out_trade_no : str = Field(alias="trade_id")
    transaction_id : str = ""
    payment_time_text : Optional[datetime]
    commodity_list: List[Product] = []

class postOproduct(BaseModel):
    oid : int 
    pid : int = Field(alias="id")
    p_name : str = Field(alias="name")
    price : Decimal = Decimal("0.00")
    quantity : int = Field(alias="number")
    is_takeout : bool = Field(default=0, alias="is_out")
    is_refund : int = 0

class postOrder(BaseModel):
    status : int = 0
    torder : str = ""
    trade_id : str = ""
    remark : str = ""
    shop_num : int = 0
    open_id : str 
    phone : str = ""
    table_no : int 
    create_at : datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_price : Decimal = Field(alias="total_amount", default=Decimal("0.00"))
    commodity_list : List[postOproduct] = []