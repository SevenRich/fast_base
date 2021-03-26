# _*_ coding:utf-8 _*_

from app import create_app


application = create_app()

# 默认启动 8000 端口， debug 开启， 热加载 开启 workers 数据为 1
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='run:application', host='0.0.0.0', port=8000, reload=True, debug=True, workers=1)
