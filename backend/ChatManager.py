class ChatManager:
    """
    Manages all chats on the server
    
    Attributes:
        chat_storage (dict<int, list<string>>): A dictionary mapping chat_ids to the associated message history
    """
    def __init__(self):
        self.chat_storage = {}
    
    def create_chat(self):
        """
        Creates a new chat in chatStorage, and returns the token associated with the chat
        
        Args: 
            None
        Returns:
            token (string): A web token assigned to each chat/user. Contains a valid chat_id (int)
        """
        raise NotImplementedError()
    
    def validate_token(self, token):
        """
        Ensures that the provided token is valid
        
        Args:
            token (string): The web token to be validated
            
        Returns:
            is_valid (bool): Whether the token is valid or not
        """
        raise NotImplementedError()
        
    
    def validate_exp_token(self, token):
        """
        Validates whether the provided token has expired or not
        
        Args:
            token (string): The web token to validate
            
        Returns:
            is_expired (bool): True if the token has expired. False if still valid
        """
        raise NotImplementedError()
    
    def get_chat_history(self, token):
        """
        Given a token, returns the associated chat history
        
        Args:
            token (string): The user web token
            
        Returns:
            chat_history (list<string>): A chronologically ordered list of strings representing the user's chat history (includes both user and gpt responses)
        """
        raise NotImplementedError()
    
    def terminate_chat(self, token):
        """
        Terminates the chat associated with the given token by removing it from the chat_storage
        
        Args:
            token (string): The token representing which chat is being terminated
            
        Returns:
            None
        """
        raise NotImplementedError()
    
    
    
    