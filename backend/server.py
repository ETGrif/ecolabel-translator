from flask import Flask, abort, render_template, request

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
    app.run(debug=True)
