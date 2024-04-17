import requests

# --------- Boilerplate ---------

URL     = "http://labeltron.roboclub.org"
API_KEY = "c1d167d00ad642d5f3cfa750"
WIDTH   = "12mm"
SIZE    = "large"

def print_label(text):
    print(f"Printing: {repr(text)}")
    resp = requests.post(URL+"/print_one_api", {
        "width": WIDTH, "size": SIZE,
        "apikey": API_KEY, "text": text
    })
    if resp.status_code != 200:
        print("Error:", resp.text)

# --------- Your code here ---------

print_label("hello world")
print_label("hello world (again)")
