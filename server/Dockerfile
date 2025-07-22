# 官方 Python 3.11 slim 镜像
FROM python:3.11-slim

WORKDIR /app

# 复制 requirements.txt 并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口 本项目用fastAPI 8000，冲突自行修改
EXPOSE 8000

# PROD：
# fastAPI服务启动命令，生产环境不加 reload
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# DEV：
# fastAPI服务启动命令，开发环境加 reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]