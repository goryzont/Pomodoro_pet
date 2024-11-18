from redis import asyncio as redis

def get_redis_connection() -> redis.Redis:
    return  redis.Redis(
        host='localhost',
        port=6378,
        db=0,
    )

def set_pomodor_count():
    redis = get_redis_connection()
    redis.json('pomodoro_count', 1)