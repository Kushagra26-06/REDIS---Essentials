"""
Redis Data Types Examples
Demonstrates all Redis data types and their operations.
"""

import redis

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def string_operations():
    """String operations - basic key-value storage."""
    print("=== String Operations ===")

    # Basic set/get
    r.set("name", "Alia")
    print(f"SET name 'Alia': {r.get('name')}")

    # Update
    r.set("name", "Riya")
    print(f"SET name 'Riya': {r.get('name')}")

    # With expiration
    r.set("session:101", "active", ex=300)
    print(f"SET with 300s TTL: {r.get('session:101')}")

    # Delete
    r.delete("name")
    print(f"After DELETE: {r.get('name')}")

    # Counter operations
    r.set("counter", 10)
    r.incr("counter")
    print(f"INCR counter: {r.get('counter')}")
    r.incrby("counter", 5)
    print(f"INCRBY 5: {r.get('counter')}")

    r.delete("session:101", "counter")


def hash_operations():
    """Hash operations - storing objects."""
    print("\n=== Hash Operations ===")

    # Store user object
    r.hset("user:1", mapping={
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    })

    # Get single field
    print(f"HGET name: {r.hget('user:1', 'name')}")

    # Get all fields
    print(f"HGETALL: {r.hgetall('user:1')}")

    # Update field
    r.hset("user:1", "age", 31)
    print(f"HSET age 31: {r.hget('user:1', 'age')}")

    r.delete("user:1")


def list_operations():
    """List operations - queues and stacks."""
    print("\n=== List Operations ===")

    # Add to list
    r.lpush("queue", "task1", "task2", "task3")
    r.rpush("queue", "task4")

    # Get all elements
    print(f"LRANGE all: {r.lrange('queue', 0, -1)}")

    # Pop from left (FIFO)
    print(f"LPOP: {r.lpop('queue')}")

    # Pop from right (LIFO)
    print(f"RPOP: {r.rpop('queue')}")

    r.delete("queue")


def set_operations():
    """Set operations - unique collections."""
    print("\n=== Set Operations ===")

    # Add elements
    r.sadd("tags", "redis", "database", "cache")
    r.sadd("tags", "redis", "fast")  # Duplicate ignored

    print(f"SMEMBERS: {r.smembers('tags')}")

    # Check membership
    print(f"SISMEMBER redis: {r.sismember('tags', 'redis')}")

    # Set operations
    r.sadd("set1", "a", "b", "c")
    r.sadd("set2", "c", "d", "e")
    print(f"SUNION: {r.sunion('set1', 'set2')}")
    print(f"SINTER: {r.sinter('set1', 'set2')}")

    r.delete("tags", "set1", "set2")


def sorted_set_operations():
    """Sorted set operations - leaderboards."""
    print("\n=== Sorted Set Operations ===")

    # Add with scores
    r.zadd("leaderboard", {
        "player1": 100,
        "player2": 200,
        "player3": 150
    })

    # Get with scores (high to low)
    print(f"ZREVRANGE: {r.zrevrange('leaderboard', 0, -1, withscores=True)}")

    # Get rank
    print(f"ZREVRANK player2: {r.zrevrank('leaderboard', 'player2')}")

    # Update score
    r.zincrby("leaderboard", 50, "player1")
    print(f"ZINCRBY player1 50: {r.zscore('leaderboard', 'player1')}")

    r.delete("leaderboard")


if __name__ == "__main__":
    string_operations()
    hash_operations()
    list_operations()
    set_operations()
    sorted_set_operations()
    print("\n=== All data type examples completed ===")
