import time

def is_rate_limited(user_last_call: dict, user_id: int, cooldown: int) -> bool:
    now = time.time()
    if user_id in user_last_call:
        return now - user_last_call[user_id] < cooldown
    return False
