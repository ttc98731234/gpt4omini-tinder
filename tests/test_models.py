
import unittest
from unittest.mock import patch, MagicMock
from src.models import OpenAIModel


class TestOpenAIModel(unittest.TestCase):
    def setUp(self):
        self.api_key = 'test_api_key'
        self.model_engine = 'gpt-4o-mini'
        self.image_size = '1024x1024'
        self.model = OpenAIModel(self.api_key, self.model_engine, self.image_size)

    @patch('openai.OpenAI')
    def test_chat_completion(self, mock_openai):
        # Setup mock response
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "Test response"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        
        mock_client.chat.completions.create.return_value = mock_response
        
        # Test the method
        messages = [{'role': 'user', 'content': 'Test prompt'}]
        result = self.model.chat_completion(messages)
        
        # Verify the method was called correctly
        mock_client.chat.completions.create.assert_called_once_with(
            model=self.model_engine,
            messages=messages,
            temperature=0.7,
            max_tokens=None
        )
        
        # Verify the result
        self.assertEqual(result['choices'][0]['message']['content'], "Test response")

    @patch('openai.OpenAI')
    def test_image_generation(self, mock_openai):
        # Setup mock response
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_response = MagicMock()
        mock_data = MagicMock()
        mock_data.url = "Test URL"
        mock_response.data = [mock_data]
        
        mock_client.images.generate.return_value = mock_response
        
        # Test the method
        prompt = "Test prompt"
        result = self.model.image_generation(prompt)
        
        # Verify the method was called correctly
        mock_client.images.generate.assert_called_once_with(
            prompt=prompt,
            n=1,
            size=self.image_size,
            quality="standard"
        )
        
        # Verify the result
        self.assertEqual(result, "Test URL")


if __name__ == '__main__':
    unittest.main()
