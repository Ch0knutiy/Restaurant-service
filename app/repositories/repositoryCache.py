import redis_connection


def set_cache(key: str, value: str) -> None:
    redis_connection.r.set(key, value, 120)


def get_cache(key: str) -> str:
    return redis_connection.r.get(key)


def del_cache(key: str) -> None:
    redis_connection.r.delete(key)


def flush() -> None:
    redis_connection.r.flushall()
