"""
Redis Common Use Cases
Demonstrates practical implementations of Redis patterns.
"""

import redis
import json
import uuid

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


# 1. Caching
def caching_example():
    """Cache-aside pattern for database caching."""
    print("=== Caching Example ===")

    def get_user(user_id):
        cache_key = f"user:{user_id}"
        cached = r.get(cache_key)

        if cached:
            print("Cache hit!")
            return json.loads(cached)

        # Simulate DB fetch
        print("Cache miss, fetching from DB...")
        user_data = {"id": user_id, "name": "John Doe", "email": "john@example.com"}
        r.setex(cache_key, 300, json.dumps(user_data))  # 5 min TTL
        return user_data

    # First call - cache miss
    user = get_user(1)
    print(f"User: {user}\n")

    # Second call - cache hit
    user = get_user(1)
    print(f"User: {user}\n")

    r.delete("user:1")


# 2. Session Storage
def session_storage_example():
    """Store user sessions with auto-expiration."""
    print("=== Session Storage Example ===")

    def create_session(user_data):
        session_id = str(uuid.uuid4())
        r.setex(f"session:{session_id}", 1800, json.dumps(user_data))  # 30 min
        return session_id

    def get_session(session_id):
        data = r.get(f"session:{session_id}")
        return json.loads(data) if data else None

    session_id = create_session({"user_id": 1, "name": "John"})
    print(f"Session created: {session_id}")

    session = get_session(session_id)
    print(f"Session data: {session}\n")

    r.delete(f"session:{session_id}")


# 3. Rate Limiting
def rate_limiting_example():
    """Rate limiting using sliding window."""
    print("=== Rate Limiting Example ===")

    def is_rate_limited(user_id, limit=5, window=60):
        key = f"rate_limit:{user_id}"
        current = r.incr(key)
        if current == 1:
            r.expire(key, window)
        return current > limit

    for i in range(7):
        if is_rate_limited("user123", limit=5):
            print(f"Request {i+1}: Rate limited!")
        else:
            print(f"Request {i+1}: Allowed")

    r.delete("rate_limit:user123")
    print()


# 4. Leaderboard
def leaderboard_example():
    """Game leaderboard using sorted sets."""
    print("=== Leaderboard Example ===")

    # Add scores
    r.zadd("game:leaderboard", {"alice": 1000, "bob": 1500, "charlie": 1200})

    # Get top players
    top_players = r.zrevrange("game:leaderboard", 0, 2, withscores=True)
    print("Top 3 players:")
    for rank, (player, score) in enumerate(top_players, 1):
        print(f"  {rank}. {player}: {score}")

    # Get player rank
    rank = r.zrevrank("game:leaderboard", "bob")
    print(f"\nBob's rank: {rank + 1}\n")

    r.delete("game:leaderboard")


# 5. Simple Queue
def queue_example():
    """Job queue using lists."""
    print("=== Queue Example ===")

    # Enqueue tasks
    r.rpush("task_queue", json.dumps({"type": "email", "to": "user@example.com"}))
    r.rpush("task_queue", json.dumps({"type": "report", "id": 123}))
    print("Enqueued 2 tasks")

    # Dequeue and process
    for _ in range(2):
        task = r.lpop("task_queue")
        if task:
            print(f"Processing: {json.loads(task)}")

    print()


# 6. Unique Count (HyperLogLog)
def hyperloglog_example():
    """Approximate unique counting."""
    print("=== HyperLogLog Example ===")

    # Add visitors (duplicates ignored)
    r.pfadd("visitors", "user1", "user2", "user3")
    r.pfadd("visitors", "user2", "user4", "user5")

    count = r.pfcount("visitors")
    print(f"Approximate unique visitors: {count}")
    print("Memory usage: ~12KB regardless of count!\n")

    r.delete("visitors")


if __name__ == "__main__":
    caching_example()
    session_storage_example()
    rate_limiting_example()
    leaderboard_example()
    queue_example()
    hyperloglog_example()
    print("=== All use case examples completed ===")
