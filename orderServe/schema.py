from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

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
    is_takeout : int = 0
    status : int = 0
    shop_num : int = 0
    price : Decimal = Field(default=Decimal("0.00"), alias="total_price") 
    commodity_list: List[Product] = []

class comOrder(BaseModel):
    id : int
    status : int = 0
    shop_num : int = 0
    price : Decimal = Field(default=Decimal("0.00"), alias="total_price") 
    remark : str = ""
    out_trade_no : str = ""
    transaction_id : str = ""
    payment_time_text : Optional[datetime]
    commodity_list: List[Product] = []