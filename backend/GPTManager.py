class GPTManager:
    """
    Handles all interactions with OpenAI/GPT
    
    Attributes:
        api_key (string): A string representing the OpenAI key being used
    """
    def __init__(self, api_key):
        self.api_key = api_key
    
    def get_resp(self, prompt):
        """
        Sends the given prompt to OpenAI and retrieves the response
        
        Args:
            prompt (string): The full string prompt to give to OpenAI

        Returns:
            response (string): The response from OpenAI
        """
        raise NotImplementedError()