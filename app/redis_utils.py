def delete_pattern(redis_client, pattern):
    cursor = '0'
    while cursor != 0:
        cursor, keys = redis_client.scan(cursor=cursor, match=pattern)
        if keys:
            redis_client.delete(*keys)
