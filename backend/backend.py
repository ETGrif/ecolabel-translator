import DBManager as dbm
import ChatManager as cm
import GPTManager as gptm

import dotenv as denv

denv_file = "backend/config.env"
denv_secret = "backend/secret.env"

# managers
dbMan, chatMan, gptMan = 0,0,0


def init_system():
    dbMan = dbm.DBManager(denv.get_key(denv_file, "DB_FILE"))
    chatMan = cm.ChatManager()
    gptMan = gptm.GPTManager(denv.get_key(denv_secret, "OPEN_AI_API_KEY"))
    

def search():
    raise NotImplementedError()

def init_chat():
    raise NotImplementedError()

def get_resp():
    raise NotImplementedError()

def terminate_chat():
    raise NotImplementedError()


# TODO: clean up the part that makes this run normally
# The setup
init_system()