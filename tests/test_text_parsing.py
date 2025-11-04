def test_strip_bot_mention():
    bot_id = 999
    full_message = f"<@{bot_id}> What is type effectiveness?"
    stripped = full_message.replace(f"<@{bot_id}>", "").strip()
    assert stripped == "What is type effectiveness?"
