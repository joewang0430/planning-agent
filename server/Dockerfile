# official Python 3.11 slim img
FROM python:3.11-slim

WORKDIR /app

# copy requirements.txt and dependencies installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app code 
COPY . .

# expose port fastAPI 8000, change if conflict
EXPOSE 8000

# fastAPI start，production ? reload : no reload
# PROD：
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# DEV：
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]