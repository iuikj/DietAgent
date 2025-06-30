FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY pyproject.toml uv.lock ./

# 安装uv包管理器
RUN pip install uv

# 安装Python依赖
RUN uv sync --frozen

# 复制应用代码
COPY . .

# 创建静态文件目录
RUN mkdir -p static

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "run_agent.py"]