
import os
from dotenv import load_dotenv
from src.models import OpenAIModel
from src.chatgpt import ChatGPT, DALLE

# Load environment variables
load_dotenv('.env')

# Initialize the model with API key and GPT-4o Mini model engine
model = OpenAIModel(
    api_key=os.getenv('OPENAI_API'), 
    model_engine=os.getenv('OPENAI_MODEL_ENGINE', 'gpt-4o-mini')
)

# Initialize ChatGPT and DALLE with the model
chatgpt = ChatGPT(model)
dalle = DALLE(model)

# Function to demonstrate ChatGPT response
def demo_chatgpt():
    user_message = "Explain the key differences between GPT-3.5 Turbo and GPT-4o Mini in three sentences."
    
    print("User: " + user_message)
    reply = chatgpt.get_response(user_message)
    print("ChatGPT: " + reply)
    print("\n" + "-"*50 + "\n")

# Function to demonstrate DALLE image generation
def demo_dalle():
    prompt = "A futuristic AI assistant helping a human, digital art style"
    
    print("Generating image with prompt: " + prompt)
    image_url = dalle.generate(prompt)
    print("Image URL: " + image_url)

# Execute the functions
if __name__ == "__main__":
    print("\n" + "="*20 + " ChatGPT Demo " + "="*20 + "\n")
    demo_chatgpt()
    
    print("\n" + "="*20 + " DALLE Demo " + "="*20 + "\n")
    demo_dalle()
