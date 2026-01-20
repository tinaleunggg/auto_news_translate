from ai_translator import AiTranslator
import pytest
import aiohttp
from unittest.mock import patch, AsyncMock
from aioresponses import aioresponses
import json

response_body = '''{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "At its core, Artificial Intelligence works by learning from vast amounts of data ..."
          }
        ],
        "role": "model"
      },
      "finishReason": "STOP",
      "index": 1
    }
  ]
}'''

@pytest.fixture()
def Ai(scope = "module"):
    return AiTranslator()
        
@pytest.fixture
def mock_aioresponse():
    with aioresponses() as mock:
        yield mock

def test_prompt(Ai):
    prompt = Ai.generate_prompt("test title", "test content")
    assert "test title" in prompt
    assert "test content" in prompt

@pytest.mark.asyncio    
async def test_mock_process_article(Ai, mock_aioresponse):
    mock_aioresponse.post(Ai.API_URL, status=200, payload=json.loads(response_body))
    async with aiohttp.ClientSession() as session:
        response = await Ai.process_article("test title", "test content", session)
        assert response and type(response) == str and len(response) > 0
        
@pytest.mark.asyncio
async def test_raise(Ai, mock_aioresponse):
    mock_aioresponse.post(Ai.API_URL, status=500, payload={"error": "testing error"})
    new_Ai = AiTranslator()
    with pytest.raises(aiohttp.ClientResponseError):
        async with aiohttp.ClientSession() as session:
            response = await new_Ai.process_article("test title", "test content", session)