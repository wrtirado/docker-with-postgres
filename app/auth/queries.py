# imports forgenerate_auth_code function
import random
import redis
from datetime import timedelta

# Connect to Redis
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)


def generate_auth_code(email: str) -> str:
    # Generate a random 6-digit number
    auth_code = str(random.randint(100000, 999999))
    # Store the auth code in Redis with a 5-minute expiration
    redis_client.setex(f"auth_code:{email}", timedelta(minutes=5), auth_code)
    return auth_code
