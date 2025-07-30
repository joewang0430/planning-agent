# Planning Agent Project Setup Guide

This guide will help you set up and run the Planning Agent project locally.

## Prerequisites

- [Git](https://git-scm.com/downloads)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [VS Code](https://code.visualstudio.com/) (optional, recommended)

## 1. Clone the Repository

```bash
git clone <your-repo-url>
cd planning-agent
```

## 2. Configure Frontend Environment Variables

Create a `.env.local` file in the `client` folder:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```


## 2b. Configure Backend Environment Variables

Create a `.env` file in the `server` folder and add your AI API Key, url, and model name:

```
API_KEY=your_api_key_here
BASE_URL=https:your-url-here
MODEL_NAME=your_model_name_here
FRONTEND_URL=http://localhost:3000

# For knowledge base vectorization (embedding)
EBD_API_KEY=your_embedding_api_key
EBD_BASE_URL=https://your-embedding-api-url
EBD_MODEL_NAME=your_embedding_model_name
```

---

## 2c. Initialize Knowledge Base and Run Vectorization

1. **Prepare your knowledge base files**
   - Place your XML knowledge files in the `server/app/kb/data` directory, organized by category if needed.
   - Example structure:
     ```
     server/app/kb/data/
       ├── 01_组织机构/
       │     ├── 文件1.xml
       │     └── 文件2.xml
       └── 02_政策法规/
             └── 文件3.xml
     ```

2. **Configure embedding environment variables**
   - In your `server/.env` file, ensure you have:
     ```
     EBD_API_KEY=your_embedding_api_key
     EBD_BASE_URL=https://your-embedding-api-url
     EBD_MODEL_NAME=your_embedding_model_name
     ```

3. **Run the vectorization script**
   - In the `server/app/kb` directory, run:
     ```bash
     python vectorization.py
     ```
   - This will parse your XML files, generate embeddings, and save the results to `server/app/kb/vector_data/`.
   - Output files:
     - `kb_vectors.npy`: the embedding vectors
     - `kb_meta.json`: metadata mapping each vector to its source file

---

## 3. Run the Project in Docker

Make sure Docker Desktop is running.

In the project root directory, run:

```bash
docker-compose up --build
```

- The frontend (Next.js) will be available at: http://localhost:3000
- The backend (FastAPI) API will be available at: http://localhost:8000

## 4. Useful Docker Commands

- Stop all services:
  ```bash
  docker-compose down
  ```
- Rebuild images:
  ```bash
  docker-compose build
  ```
- View logs:
  ```bash
  docker-compose logs
  ```

## 5. Troubleshooting

- **Port already in use:**
  If you see an error like `address already in use`, free the port:
  ```bash
  lsof -i :3000
  kill -9 <PID>
  lsof -i :8000
  kill -9 <PID>
  ```
- **Dependency errors:**
  If you see errors about missing modules, rebuild the containers:
  ```bash
  docker-compose build
  docker-compose up
  ```

- **API or `useEffect` Called Twice in Development:**
  If you notice that API calls or `useEffect` hooks are running twice when a component mounts, this is **expected behavior** in the Next.js development environment. It is caused by React's `StrictMode`, which intentionally mounts, unmounts, and re-mounts components to help you find bugs related to side-effects. This behavior **will not occur in the production build**. If you need to disable it for specific debugging purposes (not recommended), you can do so in `client/next.config.js`:
  ```javascript
  /** @type {import('next').NextConfig} */
  const nextConfig = {
    reactStrictMode: false,
  };

  module.exports = nextConfig;
  ```

---

**You do NOT need to install Node.js or Python locally. All code runs inside Docker containers.**
Create a `.env.local` file in the `client` folder:
NEXT_PUBLIC_API_URL=http://localhost:8000


## 3. Run the Project in Docker

Make sure Docker Desktop is running.

In the project root directory, run:

```bash
docker-compose up --build

- The frontend (Next.js) will be available at: http://localhost:3000
- The backend (FastAPI) API will be available at: http://localhost:8000

## 4. Useful Docker Commands

- Stop all services:
```bash
docker-compose down

- Rebuild images:
```bash
docker-compose build

- View logs:
```bash
docker-compose logs

## 5. Troubleshooting
- Port already in use:
If you see an error like address already in use, free the port: