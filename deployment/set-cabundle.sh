#!/bin/bash
export CA_BUNDLE=$(kubectl config view --raw --minify --flatten -o jsonpath='{.clusters[].cluster.certificate-authority-data}')

sed -i "s|\${CA_BUNDLE}|${CA_BUNDLE}|g" webhook.yaml
