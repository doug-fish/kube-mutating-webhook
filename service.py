from flask import Flask
app = Flask(__name__)

@app.route('/services')
@app.route('/services/')
def service():
  print("entering /services")
  return "<div>Hi!</div>"

@app.route('/mutate', methods=['POST'])
def mutate(path):
  print("entering /mutate")
  content=response.get_json()
  print("
  data=content
  response = app.response_class(
    response=json.dumps(data),
    status=200,
    mimetype='application/json'
  )
  print("mutate response:")
  print(response)
  print("exiting /mutate")
  return response

@app.route('/<path:path>')
def default(path):
  print("entering %s" % path)
  return "<div>Oh?</div>"
