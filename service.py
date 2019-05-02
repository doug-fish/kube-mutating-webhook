from flask import Flask
from flask import request
import json

app = Flask(__name__)

@app.route('/mutate', methods=['POST'])
def mutate():
  print("entering /mutate")
  content=request.get_json()
  print(content)
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

@app.route('/<path:path>', methods=['POST', 'GET'])
def default(path):
  print("entering %s" % path)
  response = app.response_class(
    response=json.dumps({"error": "path not found"}),
    status=404,
    mimetype='application/json'
  )
  return response
