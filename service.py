from flask import Flask
from flask import request
import json

app = Flask(__name__)

@app.route('/mutate', methods=['POST'])
def mutate():
  print("entering /mutate")
  requestData=request.get_json() or {}
  print(requestData)
  type=requestData.get('request', {}).get('object', {}).get('spec', {}).get('type','')
  annotations=requestData.get('request', {}).get('object', {}).get('metadata', {}).get('annotations',{})
  annotation=annotations.get('service.beta.kubernetes.io/azure-load-balancer-internal', '')
  noAnnotation = not annotation.lower() == "true"
  print ("type: %s" % type)
  print ("annotations: %s" % annotations)
  print ("noAnnotation: %s" % noAnnotation)
  print ("equal loadbalander?: %s" % type.lower() == "loadbalancer")

  # array of json patch operations RFC 6902
  patchOperations = []

  if type.lower() == "loadbalancer" and noAnnotation:
    print("will update")
    # if an annotation exists, remove it
    if annotation:
        patchOperations.append({"op": "remove",
                             "path": "/metadata/annotations/service.beta.kubernetes.io\/azure-load-balancer-internal"})
    # add in a proper annotation
    patchOperations.append({"op": "add",
                         "path": "/metadata/annotations",
                         "value": {}})
    
    patchOperations.append({"op": "add",
                         "path": "/metadata/annotations/test",
                         "value": "success"})
    patchOperations.append({"op": "add",
                         "path": "/metadata/annotations/service.beta.kubernetes.io\/azure-load-balancer-internal",
                         "value": "true"})
  else:
    print("no update needed")

  #https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/api/admission/v1beta1/types_swagger_doc_generated.go
  responseJson = {
    "uid": requestData.get("request", {}).get("uid", 0),
    "allowed": "true",
    "status": "",
    "patch": patchOperations, #RFC 6902 JSON Patch
    "patchType": "JSONPatch"
  }
  
  responseJsonString = json.dumps(responseJson)
  print("response body: %s" % responseJsonString)

  response = app.response_class(
  #https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/api/admission/v1beta1/types_swagger_doc_generated.go
    response=responseJsonString,
    status=200,
    mimetype='application/json'
  )
  print("mutate response:")
  print(response)
  print("exiting /mutate", flush=True)
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
