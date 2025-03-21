
class Dialog:
    def __init__(self):
        self.prefix = """
I want you to act as my Tinder assistant. I'll provide you with conversation history between me and my match on Tinder.
Your task is to help me reply to my match in a friendly, engaging way that continues the conversation naturally.
If there's a question from the match, try to answer it and then ask a follow-up question.
Keep responses relatively short (1-3 sentences) and conversational in tone.
If you think an appropriate response includes an emoji, include it.
Start your message with [Sender] so I know it's meant to be sent.
        """
    
    def generate_input(self, from_user_id, to_user_id, messages):
        conversation_history = ""
        for message in messages:
            if message.from_id == from_user_id:
                sender = "Me"
            else:
                sender = "Match"
            conversation_history += f"{sender}: {message.message}\n"
        
        prompt = f"{self.prefix}\n\nConversation history:\n{conversation_history}\n\nPlease help me reply to my match:"
        return prompt
