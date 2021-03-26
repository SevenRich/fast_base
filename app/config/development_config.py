#!/usr/bin/python3
# _*_ coding:utf-8 _*_
# __author__ = '__Chris__'

# 系统组件
import os

# 第三方组件
from typing import List
from pydantic import BaseSettings, EmailStr, AnyHttpUrl

class Settings(BaseSettings):
    # 项目根路径
    BASE_PATH: str = os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))
    
    PROJECT_NAME: str = 'Code Generation System!'
    DESCRIPTION: str = ''
    
    # 调试模式
    DEBUG: bool = True
    
    # 文档配置
    DOC_TITLE: str = "Code Generation System!"
    DOC_DESCRIPTION: str = "Code Generation System V1.0.0!"
    DOC_VERSION: str = "V1.0.0"
    
    # 项目
    PROJECT_NAME: str = "Code Generation System!"
    
    #
    SERVER_HOST: str = ''
    API_V1_STR: str = "/api/v1"
    # SECRET_KEY 记得保密生产环境 不要直接写在代码里面
    SECRET_KEY: str = "(-ASp+_)-Ulhw0848hnvVG-iqKyJSD&*&^-H3C9mqEqSl8KN-YRzRE"

    # 跨域设置 验证 list包含任意http url
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:8080",
    ]
    
    # 验证邮箱地址格式
    FIRST_MALL: EmailStr = "sevenrich@163.com"
    
    FIRST_SUPERUSER: str = "sevenrich@163.com"
    FIRST_SUPERUSER_PASSWORD: str = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
    
    # 默认数据库
    SQLALCHEMY_DATABASE_URI: str = "postgresql+psycopg2://postgres:root@192.168.0.200:15432/test_alembic"
    
    # oauth 2.0
    # 通过openssl rand -hex 32 生成的秘钥
    OAUTH_SECRET_KEY: str = "a219acf47da772621cd951f804cc0cfc57bb5b7731f97d9b45559aca09d4779f"
    OAUTH_ALGORITHM: str = "HS256" # 加密签名算法
    # token过期时间 60 minutes * 24 hours * 8 days = 8 days
    OAUTH_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    OAUTH_TOKEN_URL: str = "access-token"  # 获取token的URL
    
    # email
    SMTP_HOST: str = "smtp.exmail.qq.com"
    SMTP_PORT: int = 465
    SMTP_TLS: bool = False
    SMTP_USER: EmailStr = "service@sanren.work"
    SMTP_PASSWORD: str = "UBoh8B2PaTih7v3G"
    
    EMAILS_FROM_NAME: str = "service"
    EMAILS_FROM_EMAIL: EmailStr = "service@sanren.work"
    EMAILS_ENABLED: bool = True
    
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "app/email-templates/build"
    

# 实例化配置对象
settings = Settings()
