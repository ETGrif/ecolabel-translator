class GPTManager:
    
    def __init__(self, api_key):
        self.api_key = api_key
    
    def get_resp(self, prompt):
        raise NotImplementedError()