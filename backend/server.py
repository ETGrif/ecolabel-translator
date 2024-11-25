from flask import Flask, abort, render_template, request, jsonify
import DBManager as dbm
import ChatManager as cm
import GPTManager as gptm
from flask_cors import CORS
import dotenv as denv
import signal

denv_file = "backend/config.env"
denv_secret = "backend/secret.env"

# managers
dbMan, chatMan, gptMan = 0,0,0

def graceful_shutdown(signal, frame):
    print("shutting down...")
    dbMan.close_database_connection()
    exit(0)


signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)
app = Flask(__name__)
CORS(app)


@app.errorhandler(501)
def not_implemented(error):
    return render_template("not_implemented.html", path=request.path), 501


@app.route("/search", methods=["GET"])
def search():
    q = request.args.get("q", 0)
    if q == 0: abort(422) #verify that the arg was included
    results = dbMan.search_ecolabels_by_name(q)
    
    resp = {"eco_label_data":[]}
    
    for r in results:
        if len(resp["eco_label_data"]) < 3:
            resp["eco_label_data"].append({
                "eco_label": r["name"],
                "image_url": r["image_url"],
                "description": r["short_description"]
            })
    
    default_resp = {
        "eco_label_data": [
            {
                "eco_label": "label_1",
                "image_url": "https://dummyimage.com/600x400/ff0000/fff.jpg&text=label_1",
                "description": "lorem ipsum"
            },
            {
                "eco_label": "label_2",
                "image_url": "https://dummyimage.com/600x400/00ff00/fff.jpg&text=label_2",
                "description": "dolor sit amet"
            },
            {
                "eco_label": "label_3",
                "image_url": "https://dummyimage.com/600x400/0000ff/fff.jpg&text=label_3",
                "description": "consectetur"
            }
        ]
    }  
    
    
    return resp


@app.route("/chat/init", methods=["GET"])
def chat_init():
   label = request.args.get("label", 0)
   if label == 0: abort(422)
   
   token = chatMan.create_chat()
   
#    connect this to the DB
   response = dbMan.get_ecolabel_by_name(label)
   
   label_info = {
       "name": response["name"],
       "description": response["description"]
   }
   
#    set up the chat   
   [sysMessage,userMessage] = gptMan.init_chat(label_info)   
   chatMan.add_record(token, sysMessage[1], sysMessage[0])   
   chatMan.add_record(token, userMessage[1], userMessage[0])
   
#    get the message
   chat = chatMan.get_chat(token)
   message = gptMan.get_resp(chat)
   
#    save the message
   chatMan.add_record(token, message, "assistant")
   
#    respond!
   resp = {
       "assistant_message": message,
       "chat_token": token
   }
   
   return resp


@app.route("/chat/send", methods=["GET"])
def chat_send():
    token = request.args.get("t", 0)
    if token == 0: abort(422)
    
    user_message = request.args.get("m", 0)
    if user_message == 0: abort(422)
    
    try:
        chatMan.validate_token(token)
    except cm.InvalidTokenException:
        abort(401) #Unauthorized Response
        
    
    # save the message
    chatMan.add_record(token, user_message, "user")
    
    #    get the message
    chat = chatMan.get_chat(token)
    message = gptMan.get_resp(chat)
   
    # save the message
    chatMan.add_record(token, message, "assistant")
    
    resp = {
        "assistant_message": message
    }
    return resp


@app.route("/chat/terminate", methods=["PUT"])
def chat_terminate():
    token = request.args.get("t", 0)
    if token == 0: abort(422)
    
    return


if __name__ == "__main__":
    dbMan = dbm.DBManager()
    dbMan.init_database()
    chatMan = cm.ChatManager(timeout_in_min=10)
    gptMan = gptm.GPTManager(denv.get_key(denv_secret, "OPEN_AI_API_KEY"))
    
    app.run(debug=True)