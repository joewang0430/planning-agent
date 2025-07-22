# 官方 Node.js 18 Alpine 基础镜像
FROM node:18-alpine

# 设置工作目录： /app
WORKDIR /app

# 复制 package.json 和 package-lock.json 到容器中，用于安装依赖
COPY package*.json ./

# 安装项目依赖
RUN npm install

# 复制项目的全部源代码到容器工作目录
COPY . .

# Next.js 默认开发端口，按需更改
EXPOSE 3000

# 生产：先构建再启动；开发：启动，支持热载
# PROD：
# CMD ["sh", "-c", "npm run build && npm start"]
# DEV：
CMD ["npm", "run", "dev"]   