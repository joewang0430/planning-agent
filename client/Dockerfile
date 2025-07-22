# official Node.js 20 Alpine img
FROM node:20-alpine

# work directory: /app
WORKDIR /app

# copy package.json and package-lock.json into container, used to install deps
COPY package*.json ./

# install dependencies
RUN npm install

# copy all work directories
COPY . .

# Next.js default, change in need.
EXPOSE 3000

# PROD：
# CMD ["sh", "-c", "npm run build && npm start"]
# DEV：
CMD ["npm", "run", "dev"]   