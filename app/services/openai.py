from openai import OpenAI
from fastapi import HTTPException
import os

class OpenAIService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def get_chat_completion(self, prompt: str, model_name: str = "gpt-4o-mini") -> str:
        """
        Calls OpenAI's ChatCompletion API with the given prompt and returns the response.
        """
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]

        try:
            completion = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=800
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI ChatCompletion error: {str(e)}")

openai_service = OpenAIService(api_key=os.environ['OPEN_AI_KEY'])