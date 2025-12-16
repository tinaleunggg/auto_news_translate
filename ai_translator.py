import os
from dotenv import load_dotenv
import aiohttp
import asyncio
load_dotenv()

class AiTranslator:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    AI_MODEL = 'gemini-2.5-flash'
    API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/{AI_MODEL}:generateContent'
    
    def __init__(self):
        pass
    
    def generate_prompt(self, title, content):
        return f"""你是一個專業的中文新聞編輯。請用繁體中文總結新聞內容，包含重點摘要和關鍵信息。
        請總結以下新聞內容：

        標題：{title}

        內容：{content}

        請提供：
        1. 標題
        2. 重點摘要
        3. 關鍵信息

        備註: 回覆只需以上三點, 不需要說: 好的,作為..現在為你..
        """
        
    async def process_article(self, content, title):
        try:
            print(f'🤖 Processing with Gemini AI: {title[:50]}...')
            
            prompt = self.generate_prompt(title, content)
           
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "maxOutputTokens": 5000,
                }
            }
            headers = {
                'Content-Type': 'application/json',
                'x-goog-api-key': self.GEMINI_API_KEY
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(self.API_URL, json=payload, headers=headers) as response:
                    if response.status != 200:
                        raise ConnectionError(f'HTTP {response.status}')
                    
                    data = await response.json()
                    
                    print(data)
                    
                    if data.get('candidates') and len(data['candidates']) > 0:
                        generated_text = data['candidates'][0]['content']['parts'][0]['text']
                        print('✅ Gemini AI processing successful')
                        return generated_text
                    else:
                        raise ValueError('No response from Gemini API')
                    
        except Exception as error:
            print(f'❌ Gemini AI processing error: {error}')
            return '無法處理此新聞內容 - Gemini AI 處理失敗'
        
    async def test_generate(self, text):
        try:
            print(f'🤖 Testing with Gemini AI: ...')
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": text
                    }]
                }],
                "generationConfig": {
                    "maxOutputTokens": 100,
                }
            }
            headers = {
                'Content-Type': 'application/json',
                'x-goog-api-key': self.GEMINI_API_KEY
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.API_URL, json=payload, headers=headers) as response:
                    if response.status != 200:
                        raise ConnectionError(f'HTTP {response.status}')
                    
                    data = await response.json()
                    
                    print(data)
                    
                    if data.get('candidates') and len(data['candidates']) > 0:
                        generated_text = data['candidates'][0]['content']['parts'][0]['text']
                        print('✅ Gemini AI processing successful')
                        return generated_text
                    else:
                        raise ValueError('No response from Gemini API')
                    
        except Exception as error:
            print(f'❌ Gemini AI processing error: {error}')
            return '無法處理此新聞內容 - Gemini AI 處理失敗'
        
        
        
if __name__ == "__main__":
    async def main():
        ai = AiTranslator()
        await ai.test_generate("Hello, this is testing")
    asyncio.run(main())