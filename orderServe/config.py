from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    WECHAT_APP_ID: str = ""
    WECHAT_APP_SECRET: str = ""
    DATABASE_URL: str = ""
    DATABASE_NAME: str = ""
    DATABASE_USERNAME: str = ""
    DATABASE_PASSWORD: str = ""
    SECRET_KEY: str = ""
    SIGN_ALGORITHM: str = ""
    class Config:
        # 指定从 .env 文件读取（可选）
        env_file = ".env"
        env_file_encoding = "utf-8"


# 创建一个全局配置实例
settings = Settings()