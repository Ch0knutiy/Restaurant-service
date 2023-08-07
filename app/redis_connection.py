import redis  # type ignore

r = redis.Redis(host='y_lab_redis', port=6379, decode_responses=True, )


def get_redis():
    return r


# def close_redis():
#     r.close()
