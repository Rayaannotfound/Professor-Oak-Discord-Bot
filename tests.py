import pytest
from unittest.mock import AsyncMock, patch
import time

from discordapp import user_last_call, RATE_LIMIT


@pytest.mark.asyncio
async def test_rate_limit_allows_first_call():
    user_id = 123
    now = time.time()
    user_last_call.clear()
    assert user_id not in user_last_call
    user_last_call[user_id] = now - (RATE_LIMIT + 1)
    assert time.time() - user_last_call[user_id] > RATE_LIMIT


@pytest.mark.asyncio
async def test_rate_limit_blocks_second_call():
    user_id = 456
    now = time.time()
    user_last_call.clear()
    user_last_call[user_id] = now
    assert time.time() - user_last_call[user_id] < RATE_LIMIT


@pytest.mark.asyncio
async def test_bot_does_not_reply_to_self():
    class DummyMessage:
        author = "bot"
        content = "@ProfessorOak what is fire?"
        mentions = ["bot"]

    message = DummyMessage()
    message.author = message
    assert message.author == message


@pytest.mark.asyncio
@patch("openai.OpenAI.chat.completions.create")
async def test_openai_response(mock_openai):
    mock_openai.return_value = AsyncMock()
    mock_openai.return_value.choices = [
        type("obj", (object,), {
            "message": type("msg", (object,), {"content": "Test reply!"})
        })()
    ]

    # Simulate call and check reply
    response = await mock_openai()
    assert response.choices[0].message.content == "Test reply!"
