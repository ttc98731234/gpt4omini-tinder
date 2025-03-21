
from typing import List, Dict, Any, Optional
from openai import OpenAI


class ModelInterface:
    def chat_completion(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        pass

    def image_generation(self, prompt: str) -> str:
        pass


class OpenAIModel(ModelInterface):
    def __init__(self, api_key: str, model_engine: str = "gpt-4o-mini", image_size: str = '1024x1024'):
        self.client = OpenAI(api_key=api_key)
        self.model_engine = model_engine
        self.image_size = image_size

    def chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: Optional[int] = None) -> Dict[str, Any]:
        """
        Create a chat completion using GPT-4o Mini model
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Controls randomness (0-1)
            max_tokens: Optional maximum length of response
            
        Returns:
            Dictionary containing response data
        """
        # Ensure model name has proper format with hyphen (gpt-4o-mini)
        model_name = self.model_engine
        if model_name == "gpt4o-mini":
            model_name = "gpt-4o-mini"
        
        response = self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return {
            'choices': [
                {'message': {'content': response.choices[0].message.content}}
            ]
        }

    def image_generation(self, prompt: str, quality: str = "standard") -> str:
        """
        Generate an image using DALL-E model
        
        Args:
            prompt: Text description of desired image
            quality: Image quality (standard or hd)
            
        Returns:
            URL of generated image
        """
        response = self.client.images.generate(
            prompt=prompt,
            n=1,
            size=self.image_size,
            quality=quality
        )
        image_url = response.data[0].url
        return image_url
