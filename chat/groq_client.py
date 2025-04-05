import os
import groq
from django.conf import settings

class GroqClient:
    def __init__(self):
        api_key = settings.GROQ_API_KEY
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set in environment variables")
            
        self.client = groq.Groq(
            api_key=api_key,
        )
        self.chat_model = "llama-3.2-3b-preview"  # Updated to use a supported model
        self.system_prompt = """You are a helpful AI assistant. Provide clear, accurate, and engaging responses.
        Keep responses concise but informative. Be friendly and professional."""

    def get_response(self, user_message, chat_history=None):
        try:
            messages = [
                {
                    "role": "system",
                    "content": self.system_prompt
                }
            ]

            # Add chat history if provided
            if chat_history:
                for chat in chat_history:
                    messages.append({"role": "user", "content": chat.user_message})
                    messages.append({"role": "assistant", "content": chat.bot_response})

            # Add current message
            messages.append({"role": "user", "content": user_message})

            # Get completion from Groq
            completion = self.client.chat.completions.create(
                model=self.chat_model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                top_p=1,
                stream=False
            )

            # Extract the response
            response = completion.choices[0].message.content
            return response

        except Exception as e:
            print(f"Error in Groq API call: {str(e)}")
            return "I apologize, but I'm having trouble processing your request at the moment. Please try again later." 