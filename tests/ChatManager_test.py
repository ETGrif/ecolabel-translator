import unittest
import backend.ChatManager as cm
import time


class Token_Test (unittest.TestCase):
    def test_token_validation(self):
        chatMan = cm.ChatManager(timeout_in_min=1/60)

        token = chatMan.create_chat()

        #validate non-expired token
        chat_id = chatMan.validate_token(token)
        self.assertEqual(chat_id, 1)

        time.sleep(1)

        #should be expired now (expect an exception!)
        with self.assertRaises(cm.InvalidTokenException):
            chatMan.validate_token(token)

        #validate exp token

        chat_id = chatMan.validate_exp_token(token)
        self.assertEqual(chat_id, 1)

    def test_termination(self):
        chatMan = cm.ChatManager(timeout_in_min=1/60)

        token = chatMan.create_chat()
        
        time.sleep(1)
        #token should now be expired
        chatMan.terminate_chat(token)
        
        self.assertEqual(len(chatMan.chat_logs), 0) #there should be no more logs

class Message_Test (unittest.TestCase):
    def test_message(self):
        chatMan = cm.ChatManager(.5)
        
        token = chatMan.create_chat()
            
        chatMan.add_record(token, "You are a helpfull assistant", "sys")
        chatMan.add_record(token, "Hello World!", "assistant")
        chatMan.add_record(token, "Thats crazy, man", "user")
        
        # going for an array of tuples
        log = chatMan.get_chat(token)
        
        self.assertEqual(len(chatMan.chat_logs), 1) #there is only one chat
        self.assertEqual(len(log), 3) #there are three messages in that chat
        self.assertEqual(log[0][0], "sys")
        self.assertEqual(log[0][1], "You are a helpfull assistant")
        self.assertEqual(log[1][0], "assistant")
        self.assertEqual(log[1][1], "Hello World!")
        self.assertEqual(log[2][0], "user")
        self.assertEqual(log[2][1], "Thats crazy, man")

        
        
        
        
    
        