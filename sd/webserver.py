import logging
import picoweb

logging.basicConfig(level=logging.INFO)

app = picoweb.WebApp(__name__)

@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("I can show you a table of <a href='squares'>squares</a>.")

@app.route("/squares")
def squares(req, resp):
    yield from picoweb.start_response(resp)
    yield from app.render_template(resp, "squares.tpl", (req,))

app.run(debug=True, port=80, host=wlan.ipadd, log=False)



