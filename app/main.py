from fastapi import FastAPI
import time
from prometheus_client import Counter, generate_latest
from fastapi.responses import Response
import random
import os
import psycopg2
import redis

app = FastAPI()

start_time = time.time()

@app.get("/")
def root():
    return {"message": "Cloud Platform Lab API"}

@app.get("/health")
def health():
    uptime = time.time() - start_time
    return {
        "status": "healthy",
        "uptime_seconds": uptime
    }

REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total API requests"
)

items = [
    {"id": 1, "name": "server"},
    {"id": 2, "name": "database"},
    {"id": 3, "name": "cache"}
]

@app.get("/items")
def get_items():
    REQUEST_COUNT.inc()
    return items

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

@app.get("/slow")
def slow():
    delay = random.uniform(0.2, 2.0)
    time.sleep(delay)
    return {"delay": delay}


def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "platformdb"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )
    return conn

cache = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379
)

@app.get("/cache-test")
def cache_test():
    cache.set("hello", "cloud-platform")
    value = cache.get("hello")
    return {"cache_value": value}