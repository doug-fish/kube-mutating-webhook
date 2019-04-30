from flask import Flask
app = Flask(__name__)

@app.route('/services')
@app.route('/services/')
def service():
  print("entering /services")
  return "<div>Hi!</div>"

@app.route('/<path:path>')
def default(path):
  print("entering %s" % path)
  return "<div>Oh?</div>"
