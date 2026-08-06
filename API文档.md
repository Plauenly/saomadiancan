# 七香嫂包子铺智能点餐系统 — 后端 API 接口文档

> 更新日期：2026-08-06（依据前端代码 `七香嫂包子铺智能点餐系统2` 逐接口对照更新）
>
> 前端请求基地址：`http://localhost:8080`
> Content-Type：`application/json`
> 除 `POST /api/login` 外，所有请求都必须携带请求头：`Authorization: Bearer <token>`
> token 由登录接口返回，前端存于本地 storage（key: `token`）
> 401 处理：前端检测到 401 会自动重新调用登录接口换新 token 并重试原请求一次，后端无需特殊处理

---

## ⚠️ 当前实现状态总览（后端进度）

| 接口 | 前端已调用 | 后端实现状态 |
|------|-----------|-------------|
| POST `/api/login` | ✅ | ✅ **已实现**（真实微信 code2session） |
| GET `/api/menu` | ✅ | 🚧 **开发中**（`router/menu.py` 仅建好骨架，尚未注册到 app） |
| GET `/api/banners` | ✅ | ⏳ 未实现 |
| GET `/api/user/profile` | ✅ | ⏳ 未实现（数据库 user 表已有 `phone` 字段） |
| GET `/api/user/info` | ✅（预留） | ⏳ 未实现 |
| GET `/api/orders` | ✅ | ⏳ 未实现（orders 表已建好） |
| GET `/api/orders/{id}` | ✅ | ⏳ 未实现 |
| POST `/api/orders` | ✅ | ⏳ 未实现 |
| POST `/api/orders/{id}/refund` | ✅（预留） | ⏳ 未实现 |
| POST `/api/orders/pay` | ✅ | ⏳ 未实现 |

### 🔴 已发现的前后端差异（需对齐，否则联调会出问题）

1. **登录返回格式不一致**：后端当前 `return token` 返回的是**裸字符串**（响应体为 JSON 字符串 `"eyJhbGci..."`），而前端 `auth.js` 判断的是 `r.data.token`（对象形式）。**二者必须统一**，建议后端改为 `return {"token": token}`（与前端一致，改动最小）。
2. **登录路径带不带斜杠**：后端路由是 `prefix="/api/login"` + `@login_api.post("/")`，实际路径为 **`/api/login/`（带尾斜杠）**；前端调用的是 `/api/login`（不带）。FastAPI 默认会 307 重定向，小程序端对 POST 307 的跟随行为不稳定，**建议后端把路由改为 `@login_api.post("")`**，或前端统一带斜杠。
3. **H5 调试（code 为空字符串）**：旧文档写"后端也应正常返回 token"，但当前后端会把空 code 发给微信换取 openid，微信返回错误码后后端直接 400 拒绝。**建议后端加兜底**：code 为空时直接签发一个临时 token（或返回固定测试 openid），否则 H5 开发环境无法登录。

---

## 接口总览

| # | 方法 | 路径 | 说明 | 鉴权 | 状态 |
|---|------|------|------|------|------|
| 1 | GET | `/api/menu` | 获取菜单（分类+菜品） | ✅ | 🚧 开发中 |
| 2 | GET | `/api/banners` | 获取首页轮播图 | ✅ | ⏳ |
| 3 | POST | `/api/login` | 微信登录换取 token | ❌ | ✅ 已实现 |
| 4 | GET | `/api/user/profile` | 获取当前用户手机号 | ✅ | ⏳ |
| 5 | GET | `/api/user/info` | 获取当前用户信息（预留） | ✅ | ⏳ |
| 6 | GET | `/api/orders` | 订单列表 | ✅ | ⏳ |
| 7 | GET | `/api/orders/{id}` | 订单详情 | ✅ | ⏳ |
| 8 | POST | `/api/orders` | 提交订单（下单支付） | ✅ | ⏳ |
| 9 | POST | `/api/orders/{id}/refund` | 发起退款 | ✅ | ⏳ |
| 10 | POST | `/api/orders/pay` | 继续支付（待支付订单） | ✅ | ⏳ |

---

## 3. POST `/api/login` — 微信登录（✅ 已实现）

**无需鉴权**，且不携带 Authorization 头。

**请求体：**

```json
{
  "code": "wx_login_code"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `code` | string | ✅ | `uni.login` 获取的微信登录凭证 |

**当前后端实现流程：**

1. 用 `code` 请求微信 `https://api.weixin.qq.com/sns/jscode2session`（appid/secret 在 `orderServe/.env` 中配置）
2. 微信返回 `openid`（同一小程序内永久不变）
3. 查 `user` 表：不存在则插入新用户，存在则更新 `last_login`
4. 签发 JWT（有效期 **7 天**），payload：`sub`=user_id、`openid`、`exp`；算法 HS256，密钥来自 `.env` 的 `SECRET_KEY`

**返回格式（当前实现）：**

```json
"eyJhbGciOiJIUzI1NiIs..."
```

> 🔴 当前返回的是**裸 token 字符串**，而前端 `auth.js` 期望 `{"token": "..."}` 对象，联调前必须对齐（见顶部差异提醒 #1）。

**建议返回格式（与前端对齐后）：**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**错误响应（当前实现）：**

| 状态码 | 触发条件 | detail 示例 |
|--------|---------|------------|
| 503 | 微信系统繁忙（errcode -1 / 45011） | `微信系统繁忙，请稍候重试: ...` |
| 400 | code 已过期（errcode 40029） | `请求的数据已过期，请重试: ...` |
| 400 | 高风险用户（errcode 40226） | `高风险用户，不能使用微信小程序: ...` |
| 400 | 未获取到 openid | `获取openid失败` |

> 注意：当前后端**未处理 code 为空字符串**的情况（H5 调试环境 `uni.login` 拿不到 code），会走微信接口然后返回 400。建议加兜底逻辑（见顶部差异提醒 #3）。

**说明：**
- 前端用返回的 `token` 覆盖本地存储，之后所有请求自动携带 `Authorization: Bearer <token>`
- 并发调用会被前端去重，同一时间只会发一个登录请求
- 401 时前端会自动重新登录并重试原请求一次

---

## 1. GET `/api/menu` — 获取菜单（分类+菜品）（🚧 后端开发中）

> 后端 `router/menu.py` 已建好骨架（`select * from product`），尚未完成分类/菜品/图片/标签的组装，也未注册进 `main.py`。以下为前端期望的契约，后端按此实现即可。

**无需参数**

**返回格式：** 分类数组

```json
[
  {
    "id": 1,
    "name": "招牌必吃",
    "category_image_url": "/static/img/menu/cate-1.jpg",
    "products": [
      {
        "id": 11,
        "category_id": 1,
        "name": "招牌酱肉包",
        "description": "每日现包现蒸的招牌酱肉包...",
        "images": [{ "url": "/static/img/menu/menu-1.jpg" }],
        "labels": [{ "id": 1, "name": "招牌", "color": "#FF362D" }],
        "price": 5.99,
        "status": "1",
        "is_single": true,
        "sold": "600+",
        "is_takeout": 1,
        "materials": []
      }
    ]
  }
]
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | number | 分类ID |
| `name` | string | 分类名 |
| `category_image_url` | string | 分类图标 URL（可为空，为空则不显示图标） |
| `products[].id` | number | 商品ID |
| `products[].category_id` | number | 所属分类ID（购物车会使用，建议返回） |
| `products[].name` | string | 商品名 |
| `products[].description` | string | 商品描述 |
| `products[].images` | array | 商品图片数组 `[{url}]`，前端取 `images[0].url` |
| `products[].labels` | array | 标签 `[{id, name, color}]`，可为空数组 |
| `products[].price` | number | 价格（**≤0 的商品前端禁止加购**） |
| `products[].is_single` | boolean | 是否单品（true=无配料选择，本项目无奶茶所以全为 true） |
| `products[].sold` | string | 销量展示，如 `"600+"` |
| `products[].status` | string | 商品状态：`"1"`=上架 `"0"`=下架 `"2"`=已卖完 |
| `products[].is_takeout` | number | 是否支持打包 0/1（**打包下单时会校验**） |
| `products[].materials` | array | 配料分组 `[{name, values: [{name, price}]}]` |

> 商品展示按 `status` 字段控制：`"1"` 上架正常显示，`"0"` 下架不显示，`"2"` 已卖完灰度显示且禁止加购/查看详情。

**数据库对应关系（qrOrder 库）：**

| 返回字段 | 来源表/字段 |
|---------|------------|
| 分类 id/name | `category` 表 |
| 分类-商品关联 | `category_product` 表 |
| 商品基础字段（name/description/price/sold/is_takeout） | `product` 表 |
| 商品图片 | `image_product` 表 |
| 商品标签 | `label` + `label_product` 表 |

---

## 2. GET `/api/banners` — 获取首页轮播图（⏳ 后端未实现）

**无需参数**

**返回格式：**

```json
[
  { "image_url": "/static/img/home/banner.jpg" },
  { "image_url": "https://xxx/banner2.jpg" }
]
```

**字段说明：** 数组元素支持 `image_url` 或 `image` 字段，前端优先取 `image_url`，取不到再取 `image`。请求失败或返回空数组时前端使用默认 banner 图。

---

## 4. GET `/api/user/profile` — 获取当前用户手机号（⏳ 后端未实现）

**无需参数，需鉴权**

**返回格式：**

```json
{
  "phone": "138xxxx1234"
}
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `phone` | string | 用户手机号（微信授权获取） |

> 数据库 `user` 表已预留 `phone` 字段，后端按 token 里的 `openid`/`sub` 查表返回即可。前端逻辑：首页 onShow 时若本地存在 token 则调用此接口，获取手机号后用于展示。

---

## 5. GET `/api/user/info` — 获取当前用户信息（预留）

**无需参数，需鉴权**

接口已在前端 API 映射表中定义但页面暂未调用，为后续扩展预留（如展示用户完整信息、会员等级等）。建议返回结构：

```json
{
  "id": 1,
  "nickname": "xxx",
  "avatar": "/static/logo.jpg",
  "phone": "",
  "vip_level": 0
}
```

---

## 6. GET `/api/orders` — 订单列表（⏳ 后端未实现）

**无需参数（前端已移除 type 等 query 参数），需鉴权**

**返回格式：** 订单数组

```json
[
  {
    "id": 1,
    "is_takeout": 0,
    "status": "2",
    "shop_num": 2,
    "price": 15.98,
    "commodity_list": [
      {
        "image": "/static/img/menu/menu-1.jpg",
        "name": "招牌酱肉包",
        "price": 5.99,
        "number": 2
      }
    ]
  }
]
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | number | 订单ID（前端跳详情页 `?id=` 使用） |
| `is_takeout` | number | 是否打包 0=堂食 1=打包（列表页展示"打包/堂食"角标） |
| `status` | string | 订单状态码，**字符串**：`"0"`待支付 `"1"`已支付 `"2"`制作中 `"3"`已完成 `"4"`已退款 |
| `shop_num` | number | 商品总件数 |
| `price` | number | 订单合计金额 |
| `commodity_list[]` | array | 商品列表 |
| `commodity_list[].image` | string | 商品图片 URL |
| `commodity_list[].name` | string | 商品名 |
| `commodity_list[].price` | number | 单价 |
| `commodity_list[].number` | number | 数量 |

> 数据库 `orders` 表已建好（含 status/is_takeout/remark/trade_id/transaction_id/total_price/pay_at 等字段），商品明细在 `order_product` 表。

---

## 7. GET `/api/orders/{id}` — 订单详情（⏳ 后端未实现）

**路径参数：** `id` 订单ID，需鉴权

**返回格式：**

```json
{
  "id": 1,
  "status": "2",
  "shop_num": 2,
  "price": 15.98,
  "remark": "少盐",
  "out_trade_no": "202607311234567890",
  "transaction_id": "wx4200000000000000000000000000",
  "payment_time_text": "2026-07-31 12:34:56",
  "commodity_list": [
    {
      "image": "/static/img/menu/menu-1.jpg",
      "name": "招牌酱肉包",
      "price": 5.99,
      "number": 2
    }
  ]
}
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | number | 订单ID |
| `status` | string | 状态码同订单列表，范围 `"0"` ~ `"4"` |
| `shop_num` | number | 商品总件数 |
| `price` | number | 合计金额（前端显示 `￥{{orderData.price}}`） |
| `remark` | string | 备注，可为空（前端显示"无"） |
| `out_trade_no` | string | 商户订单号（对应 orders 表 `trade_id`） |
| `transaction_id` | string | 微信交易单号 |
| `payment_time_text` | string | 支付时间（已格式化字符串，对应 `pay_at`，前端直接展示） |
| `commodity_list[]` | array | 商品列表，结构同订单列表接口 |

---

## 8. POST `/api/orders` — 提交订单（下单支付）（⏳ 后端未实现）

**请求体：**

```json
{
  "commodity_list": [
    {
      "id": 11,
      "cate_id": 1,
      "name": "招牌酱肉包",
      "price": 5.99,
      "number": 2,
      "is_takeout": 1,
      "is_refund": 0,
      "is_out": 0
    }
  ],
  "total_amount": 11.98,
  "shop_num": 2,
  "remark": "少盐"
}
```

**字段说明：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `commodity_list` | array | ✅ | 购物车商品数组（结构见下表） |
| `total_amount` | number | ✅ | 合计金额（前端已做两位小数截断） |
| `shop_num` | number | ✅ | 商品总件数 |
| `remark` | string | ❌ | 备注，可为空字符串 |

**commodity_list 元素：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | number | 商品ID |
| `cate_id` | number | 分类ID（来自菜单的 category_id） |
| `name` | string | 商品名 |
| `price` | number | 单价 |
| `number` | number | 数量 |
| `is_takeout` | number | 是否支持打包 0/1（后端应据此二次校验） |
| `is_refund` | number | 前端固定传 0 |
| `is_out` | number | 是否打包：`0`=不打包/堂食，`1`=打包（**每个商品独立选择**） |

> ⚠️ `is_out` 是每个商品粒度的（不是订单级别）。前端支持同一订单中部分商品堂食、部分打包（仅 `is_takeout=1` 的商品可设为 `is_out=1`）。后端应据此按商品维度记录就餐方式。

**返回格式：**

```json
{
  "order_id": 123
}
```

**说明：** 前端以下单成功标志为 `res.order_id` 存在。成功后前端清空本地购物车并跳转订单列表页。若需要真正的微信支付流程，可在此接口内完成统一下单，返回 `order_id` 的同时可扩展返回支付参数（如 `payment` 字段），前端暂未消费额外字段。

---

## 9. POST `/api/orders/{id}/refund` — 发起退款（⏳ 后端未实现，前端预留）

**路径参数：** `id` 订单ID，需鉴权

**请求体：**

```json
{
  "reason": "不想吃了"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `reason` | string | ❌ | 退款原因，可为空 |

**返回格式：**

```json
{
  "refund_id": 456,
  "refund_status": "processing"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `refund_id` | string/number | 退款单号 |
| `refund_status` | string | 退款状态：`"processing"`=处理中 `"success"`=已退款 `"failed"`=退款失败 |

**业务约束（建议后端校验）：**
- 仅状态为 `"1"`（已支付）或 `"2"`（制作中）的订单可发起退款
- `"0"`（待支付）无需退款；`"3"`（已完成）不可退款；`"4"`（已退款）不可重复退款
- 退款成功后该订单状态应更新为 `"4"`（已退款）

> 当前前端尚未实现退款页面，此接口为预留，后续在订单详情页会添加"申请退款"按钮。

---

## 10. POST `/api/orders/pay` — 继续支付（⏳ 后端未实现）

用于订单详情页对状态为"待支付"（`"0"`）的订单发起支付。

**请求体：**

```json
{
  "order_id": 123
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `order_id` | number | ✅ | 待支付订单的 ID |

**返回格式：**

```json
{
  "success": true
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | boolean | 支付是否成功 |
| `message` | string | 失败时的错误提示（可选） |

**前端行为（`order-detail.vue`）：**
- 仅状态为 `"0"`（待支付）的订单详情页底部显示绿色"继续支付"按钮
- 支付成功后自动刷新订单详情（重新调用 GET `/api/orders/{id}`）
- 支付失败 toast 显示 `res.message` 或默认"支付失败，请重试"

**业务约束（建议后端校验）：**
- 仅状态为 `"0"`（待支付）的订单可调用
- 其他状态的订单调用应返回 `success: false`
- 支付成功后订单状态应更新为 `"1"`（已支付）

---

## 通用约定

### 请求头

```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer <token>"
}
```

### 响应

- 前端以 **HTTP 200** 为成功判断，直接消费响应体 JSON（`res.data`），无统一包裹层（如 `{code, msg, data}`），后端请直接返回业务数据本身
- 非 200：前端统一 toast `请求失败: {statusCode}`
- 401：前端自动重新登录并重试一次，重试仍失败则 toast `登录已过期，请重新进入`
- 网络错误：前端 toast `网络错误，请稍后再试`

### 图片资源

所有 `image` / `image_url` / `category_image_url` 字段返回完整可访问 URL 即可（可走后端静态目录，如 `/img/xxx.jpg`），前端 `<u-image>` 直接加载。

> 注意：当前 `orderServe/main.py` 只 import 了 `StaticFiles` 尚未 `app.mount("/img", ...)`，图片静态目录需在后续补上（可参考 `mydemo` 里的写法）。

### 订单状态码

| 状态码 | 含义 |
|--------|------|
| `"0"` | 待支付 |
| `"1"` | 已支付 |
| `"2"` | 制作中 |
| `"3"` | 已完成 |
| `"4"` | 已退款 |

> ⚠️ 状态码为**字符串**，后端返回时注意类型，否则前端状态映射会失效（orders 表 status 字段是 tinyint，返回前需转成字符串）。

---

## 附录：后端现状（orderServe）

- **框架**：FastAPI + uvicorn，监听 `127.0.0.1:8080`（`main.py`）
- **数据库**：MySQL `qrOrder`（连接池 asyncmy，minsize=5 / maxsize=20，autocommit=True）
- **配置**：`.env` 文件（微信 appid/secret、数据库账号、JWT SECRET_KEY）
- **已建表**：`user`、`product`、`category`、`category_product`、`image_product`、`label`、`label_product`、`orders`、`order_product`
- **已实现接口**：仅 `POST /api/login/`
- **待办**：menu 接口组装与注册、banners、user 接口、orders 三件套、refund、静态图片目录挂载、登录差异对齐（见顶部 🔴 部分）
