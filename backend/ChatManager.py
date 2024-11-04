class ChatManager:
    
    def __init__(self):
        pass
    
    def create_chat(self):
        raise NotImplementedError()
    
    def validate_token(self, token):
        raise NotImplementedError()
    
    def validate_exp_token(self, token):
        raise NotImplementedError()
    
    def get_chat(self, token):
        raise NotImplementedError()
    
    def terminate_chat(self, token):
        raise NotImplementedError()
    
    
    
    