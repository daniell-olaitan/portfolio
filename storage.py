import redis
from portfolio import app


redis_client = client = redis.from_url(
    app.config['REDIS_URI'],
    decode_responses=True
)
