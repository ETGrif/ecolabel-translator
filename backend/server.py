from flask import Flask, abort, render_template, request
import DBManager as dbm
import ChatManager as cm
import GPTManager as gptm
import dotenv as denv

denv_file = "backend/config.env"
denv_secret = "backend/secret.env"

# managers
dbMan, chatMan, gptMan = 0,0,0


app = Flask(__name__)


@app.errorhandler(501)
def not_implemented(error):
    return render_template("not_implemented.html", path=request.path), 501


@app.route("/search", methods=["GET"])
def search():
    abort(501)


@app.route("/chat/init", methods=["GET"])
def chat_init():
    abort(501)


@app.route("/chat/send", methods=["GET"])
def chat_send():
    abort(501)


@app.route("/chat/terminate", methods=["PUT"])
def chat_terminate():
    abort(501)


if __name__ == "__main__":
    dbMan = dbm.DBManager(denv.get_key(denv_file, "DB_FILE"))
    chatMan = cm.ChatManager(timeout_in_min=.1)
    gptMan = gptm.GPTManager(denv.get_key(denv_secret, "OPEN_AI_API_KEY"))
    
    app.run(debug=True)
