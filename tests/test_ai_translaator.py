from ai_translator import AiTranslator
import pytest
import aiohttp



@pytest.fixture()
def Ai(scope = "module"):
    return AiTranslator()

def test_prompt(Ai):
    prompt = Ai.generate_prompt("test title", "test content")
    assert "test title" in prompt
    assert "test content" in prompt
    
@pytest.mark.asyncio    
async def test_process_article(Ai):
    async with aiohttp.ClientSession() as session:
        response = await Ai.process_article("test title", "test content", session)
        assert response and type(response) == str and len(response) > 0
        
@pytest.mark.asyncio
async def test_raise():
    new_Ai = AiTranslator()
    new_Ai.GEMINI_API_KEY = "false key"
    with pytest.raises(aiohttp.ClientResponseError):
        async with aiohttp.ClientSession() as session:
            response = await new_Ai.process_article("test title", "test content", session)