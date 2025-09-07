FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    redis-server \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN echo "bind 0.0.0.0" > /etc/redis/redis.conf && \
    echo "port 6379" >> /etc/redis/redis.conf && \
    echo "protected-mode no" >> /etc/redis/redis.conf && \
    echo "requirepass 1111" >> /etc/redis/redis.conf && \
    echo "daemonize no" >> /etc/redis/redis.conf

EXPOSE 8000 6379

CMD ["sh", "-c", "redis-server /etc/redis/redis.conf & sleep 5 && uvicorn main:app --host 0.0.0.0 --port 8000"]