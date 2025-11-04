import time
from utils.rate_limit import is_rate_limited

def test_rate_limit_blocks_within_cooldown():
    user_last_call = {123: time.time()}
    assert is_rate_limited(user_last_call, 123, cooldown=10) is True

def test_rate_limit_allows_after_cooldown():
    user_last_call = {123: time.time() - 11}
    assert is_rate_limited(user_last_call, 123, cooldown=10) is False

def test_rate_limit_allows_first_time_user():
    user_last_call = {}
    assert is_rate_limited(user_last_call, 999, cooldown=10) is False


def test_rate_limit_allows_second_time_user():
    user_last_call = {123: time.time() - 50}
    assert is_rate_limited(user_last_call, 123, cooldown=10) is False