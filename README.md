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
```

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