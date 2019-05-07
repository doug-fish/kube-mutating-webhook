import base64
import copy
from flask import Flask, jsonify
from flask import request
import json
import jsonpatch

app = Flask(__name__)

@app.route('/mutate', methods=['POST'])
def mutate():
  print("entering /mutate")
  requestData=request.get_json() or {}
  responseObject = copy.deepcopy(requestData).get('request', {}).get('object', {})
  print("requestData: %s" % requestData)
  request_field=requestData.get('request', {})
  object_field=request_field.get('object', {})
  type=object_field.get('spec', {}).get('type','')
  annotations=object_field.get('metadata', {}).get('annotations',{})
  annotation=annotations.get('service.beta.kubernetes.io/azure-load-balancer-internal', '')
  noAnnotation = not annotation.lower() == "true"
  print ("type: %s" % type)
  print ("annotations: %s" % annotations)
  print ("noAnnotation: %s" % noAnnotation)
  print ("equal loadbalander?: %s" % type.lower() == "loadbalancer")

  if type.lower() == "loadbalancer" and noAnnotation:
    print("will update")
    # if an annotation exists, remove it
    if not annotation:
      # Make sure an annotation object exists
      response_field = responseObject["metadata"]
      response_field["annotations"] = {}
    # add in the required annotation
    responseAnnotation = responseObject["metadata"]["annotations"]
    responseAnnotation["service.beta.kubernetes.io/azure-load-balancer-internal"] = "true"
  else:
    print("no update needed")

  thePatch = jsonpatch.JsonPatch.from_diff(requestData["request"]["object"], responseObject)

  print ("thePatch: %s" % thePatch)

  #https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/api/admission/v1beta1/types_swagger_doc_generated.go
  admissionResponse = {
    "uid": request_field.get("uid", 0),
    "allowed": True,
    "patch": base64.b64encode(str(thePatch).encode()).decode(),
    "patchType": "JSONPatch"
  }
  

  admissionReview = {
  #https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/api/admission/v1beta1/types_swagger_doc_generated.go
    "response": admissionResponse
  }
  print("exiting /mutate", flush=True)
  return jsonify(admissionReview)

@app.route('/<path:path>', methods=['POST', 'GET'])
def default(path):
  print("entering %s" % path)
  response = app.response_class(
    response=json.dumps({"error": "path not found"}),
    status=404,
    mimetype='application/json'
  )
  return response
