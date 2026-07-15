import os
from openai import OpenAI

class ClientHelper:
    def __init__(
        self,
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        default_model="openai/gpt-oss-120b"  # <-- Define your model here once!
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.default_model = default_model
        
        # Initialize the client right away
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )

    def get_client(self):
        """Returns the raw OpenAI client if you ever need it."""
        return self.client
