import jwt
import random as rand
import time
import unittest

class ChatManager:
        
    def __init__(self, timeout_in_min=.5):
        self.jwt_secret = str(rand.randint(0,10**10)) #create a secret to sign all tokens with (not cryptographically secure source)
        
        self.chat_id_ctr = 0
        self.chat_logs = dict()
        
        self.timeout_in_sec = int(timeout_in_min*60) #make the timout in seconds, make sure its an int
        
    
    def create_chat(self):
        #create a new chat_id
        self.chat_id_ctr+=1
        id = self.chat_id_ctr
        
        #create a new log
        self.chat_logs[id] = []
        
        #create a token
        payload = {"chat_id":id,
                  "exp":time.time()+self.timeout_in_sec} #make the expiration in the future
        token = jwt.encode(payload=payload, key=self.jwt_secret)
        
        return token
    
    def validate_token(self, token):
        #try to decode the token
        try:
            payload = jwt.decode(jwt = token, 
                                key = self.jwt_secret,
                                algorithms=["HS256"], 
                                options={
                                    "verify_signiature": True,
                                    "require":["exp", "chat_id"]
                                    })
        except jwt.ExpiredSignatureError:
            print("Expired Token")
            raise InvalidTokenException() #return false and also dummy data for the chat_id
        except jwt.InvalidTokenError as e:
            print("Invalid Token")
            print(e)
            raise InvalidTokenException()
        
        #token is not expired
        return payload["chat_id"]
        
    def validate_exp_token(self, token):
        #try to decode the token
        try:
            payload = jwt.decode(jwt = token, 
                                key = self.jwt_secret,
                                algorithms=["HS256"], 
                                options={
                                    "verify_signiature": True,
                                    "require":["exp", "chat_id"],
                                    "verify_exp": False #this is the only one thats different! Just passes over the exp
                                    })
        except jwt.ExpiredSignatureError:
            print("Expired Token")
            raise InvalidTokenException() #return false and also dummy data for the chat_id
        except jwt.InvalidTokenError as e:
            print("Invalid Token")
            print(e)
            raise InvalidTokenException()
        
        #token is not expired
        return payload["chat_id"]
    
    def add_record(self, token, message, user):
        chat_id = self.validate_token(token)
        self.chat_logs[chat_id].append((user, message))
        
    
    def get_chat(self, token):
        chat_id = self.validate_token(token)
        return self.chat_logs[chat_id]
        
        
    
    def terminate_chat(self, token):
        chat_id = self.validate_exp_token(token)
        self.chat_logs.__delitem__(chat_id)
    
    

# Custom Exceptions! Because I think it might be helpful..
class InvalidTokenException (Exception):
    pass
