from flask import Flask, render_template, request, make_response, session, redirect
from auth import setup_auth
from config import *
from render import *
from queue import *
from serial_iface import *
import threading
import logging
import time, os
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__,
            static_url_path="/res",
            static_folder="static",
            template_folder="templates")

authenticate = setup_auth()

apikey = None
apikey_created = 0

def update_apikey():
    global apikey, apikey_created
    if time.time() - apikey_created > APIKEY_EXPIRY:
        apikey = os.urandom(12).hex()
        apikey_created = time.time()
    return apikey

@app.route("/", methods=["GET"])
@authenticate
def homepage():
    key = update_apikey()
    print("Page loaded")
    return render_template("index.html", apikey=key)

@app.route("/render_preview.png", methods=["GET"])
def render_preview():
    text = request.values.get("text", "")
    if len(text) == 0: text = " "
    text = text[:400]

    image = render_png(render_label(text, border=False))

    res = make_response(image)
    res.headers["Content-Type"] = "image/png"
    return res

@app.route("/print_one_api", methods=["POST"])
def print_one_api():
    width = request.values.get("width", "12mm")
    size  = request.values.get("size", "large")
    text  = request.values.get("text", "")
    mkey  = request.values.get("apikey", "")

    if mkey != update_apikey():
        return "Invalid API key", 401

    if len(text) == 0:
        return "Invalid text", 400

    if size not in VALID_SIZES:
        return "Invalid size. Valid options: "+", ".join(VALID_SIZES), 400

    if width not in VALID_WIDTHS:
        return "Invalid width. Valid options: "+", ".join(VALID_WIDTHS), 400

    text = text[:400]
    text = width + "=//=" + size + "=//=" + text

    print(f"Adding {repr(text)} to queue")
    queue_add(text)
    return "OK"

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

threading.Thread(target=serial_loop, daemon=True).start()
threading.Thread(target=queue_loop, daemon=True).start()
 
def main():
   app.run("0.0.0.0", port=8080, debug=True)

if __name__ == "__main__":
    main()
