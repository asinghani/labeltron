from flask import Flask, render_template, request, make_response, session, redirect
from auth import setup_auth
from render import *
from queue import *
from serial_iface import *
import threading
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__,
            static_url_path="/res",
            static_folder="static",
            template_folder="templates")

authenticate = setup_auth()

@app.route("/", methods=["GET"])
@authenticate
def homepage():
    print("Page loaded")
    return render_template("index.html")

@app.route("/render_preview.png", methods=["GET"])
def render_preview():
    text = request.values.get("text", "")
    if len(text) == 0: text = " "
    text = text[:400]

    image = render_png(render_label(text, border=False))

    res = make_response(image)
    res.headers["Content-Type"] = "image/png"
    return res

@app.route("/print_one", methods=["POST"])
@authenticate
def print_one():
    text = request.values.get("text", "")
    if len(text) == 0: text = " "
    text = text[:400]

    print(f"Adding {repr(text)} to queue")
    queue_add(text)
    return "OK"

@app.route("/cancel_all", methods=["POST"])
@authenticate
def cancel_all():
    print("Cancel all")
    queue_reset()
    return "OK"

@app.route("/get_state", methods=["GET"])
@authenticate
def get_state():
    return {
        "queue": queue_get()
    }

def main():
    threading.Thread(target=serial_loop, daemon=True).start()
    threading.Thread(target=queue_loop, daemon=True).start()
    app.run("0.0.0.0", port=8080, debug=True)

if __name__ == "__main__":
    main()
