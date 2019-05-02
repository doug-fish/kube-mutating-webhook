from flask import Flask
from flask import request
import json

app = Flask(__name__)

@app.route('/mutate', methods=['POST'])
def mutate():
  print("entering /mutate")
  requestData=request.get_json() or {}
  print(requestData)
  type=requestData.get('object', {}).get('spec', {}).get('type','')
  annotations=requestData.get('object', {}).get('metadata', {}).get('annotations',{})
  annotation=annotations.get('service.beta.kubernetes.io/azure-load-balancer-internal', 'false')
  noAnnotation = not annotation.lower() == "true"

  if type.lower == "loadbalancer" and noAnnotation:
    print("will update")
  else:
    print("no update needed")

  response = app.response_class(
    response="hi",
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
