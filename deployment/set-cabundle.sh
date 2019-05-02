#!/bin/bash
export CA_BUNDLE=$(kubectl config view --raw --minify --flatten -o jsonpath='{.clusters[].cluster.certificate-authority-data}')

cat webhook.yaml | sed "s/\${CA_BUNDLE}/${CA_BUNDLE}/g"  > webhook-ready.yaml
kubectl apply -f webhook-ready.yaml
