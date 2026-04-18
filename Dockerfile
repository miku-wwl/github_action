# 1. 选择Python基础镜像：slim版本轻量稳定，无冗余内容
FROM python:3.11-slim

# 2. 设置容器内的工作目录，所有后续操作都在这个目录执行
WORKDIR /app

# 3. 把本地当前目录的所有文件（main.py等）复制到容器的/app目录
COPY . .

# 4. （可选）如果你的项目有第三方依赖，新建requirements.txt，取消下面这行注释
# RUN pip install --no-cache-dir -r requirements.txt

# 5. 容器启动时默认执行的命令：运行你的Python程序
CMD ["python", "main.py"]