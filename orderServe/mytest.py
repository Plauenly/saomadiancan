import json
from datetime import datetime,timezone
now = datetime.now().strftime("%Y%m%d%H%M%S")
print("znn_"+now+"_003")
params = {
        "appid": "WECHAT_APP_ID",
        "secret": "WECHAT_APP_SECRET",
        "js_code": "code",
        "grant_type": "authorization_code"
}
print(str(params))
print(params)
print(json.dumps(params, ensure_ascii=True, indent=4))

#;