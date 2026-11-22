"""
Redis Connection Examples
This file demonstrates different ways to connect to Redis using Python.
"""

import redis

# Basic Connection
def basic_connection():
    """Connect to Redis with basic settings."""
    r = redis.Redis(
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True  # Return strings instead of bytes
    )

    # Test connection
    try:
        r.ping()
        print("Connected to Redis successfully!")
        return r
    except redis.ConnectionError:
        print("Failed to connect to Redis")
        return None


# Connection with Authentication
def authenticated_connection():
    """Connect to Redis with password authentication."""
    r = redis.Redis(
        host="localhost",
        port=6379,
        password="yourpassword",
        db=0,
        decode_responses=True
    )

    try:
        r.ping()
        print("Connected to Redis with authentication!")
        return r
    except redis.ConnectionError:
        print("Failed to connect to Redis")
        return None


# Connection Pool
def pooled_connection():
    """Connect to Redis using connection pool (recommended for production)."""
    from redis import ConnectionPool

    # Create connection pool
    pool = ConnectionPool(
        host="localhost",
        port=6379,
        db=0,
        max_connections=50,
        decode_responses=True
    )

    # Get connection from pool
    r = redis.Redis(connection_pool=pool)

    try:
        r.ping()
        print("Connected to Redis using connection pool!")
        return r
    except redis.ConnectionError:
        print("Failed to connect to Redis")
        return None


if __name__ == "__main__":
    # Try basic connection
    print("Testing basic connection...")
    r = basic_connection()

    if r:
        # Store and retrieve a test value
        r.set("test_key", "Hello from Redis!")
        print(f"Retrieved: {r.get('test_key')}")
        r.delete("test_key")
