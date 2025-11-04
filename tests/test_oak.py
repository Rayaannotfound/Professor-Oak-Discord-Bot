import pytest
from unittest.mock import patch, AsyncMock
import discord
from handlers.oak import handle_mention

class DummyChannel:
    async def send(self, msg):
        print(f"[Mock Send] {msg}")
        self.last_message = msg

    async def typing(self):
        pass

class DummyMessage:
    def __init__(self, content):
        self.content = content
        self.channel = DummyChannel()
        self.guild = type("DummyGuild", (), {"me": type("BotUser", (), {"id": 999})})()

@pytest.mark.asyncio
@patch("handlers.oak.client.chat.completions.create")
async def test_handle_mention_calls_openai(mock_openai):
    mock_openai.return_value.choices = [
        type("choice", (), {
            "message": type("msg", (), {"content": "Test reply from Oak!"})
        })()
    ]

    message = DummyMessage("<@999> test subject")
    await handle_mention(message)

    assert "Test reply" in message.channel.last_message
