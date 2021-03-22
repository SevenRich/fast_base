# _*_ coding:utf-8 _*_

import time

# 导入 fastapi
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# 导入自定义
# 配置
from .config import settings
# 路由
from .api import api_url


# 主应用
app = FastAPI(
    title=settings.DOC_TITLE,
    description=settings.DOC_DESCRIPTION,
    version=settings.DOC_VERSION,
)

# CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTTP 查看执行时长
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Route 清单
app.include_router(api_url.api_v1_router)
