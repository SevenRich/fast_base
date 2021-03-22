# _*_ coding:utf-8 _*_

# 导入 uvicorn
import uvicorn

from app.main import app


# 默认启动 8000 端口， debug 开启， 热加载 开启 workers 数据为 1
if __name__ == '__main__':
    uvicorn.run('run:app', host='0.0.0.0', port=8000, reload=True, debug=True, workers=1)
