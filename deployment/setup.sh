openssl req -new -sha256 -key tls.key -out tls.csr -nodes -subj '/CN=internal-service-webhook-svc.default.svc.cluster.local'
echo "generated CSR:"
openssl req -noout -text -in tls.csr
echo "submitting to kube"
#kubectl create secret tls hook-tls --cert=tls.crt --key=tls.key

cat <<EOF | kubectl apply -f -
apiVersion: certificates.k8s.io/v1beta1
kind: CertificateSigningRequest
metadata:
  name: internal-service-webhook-svc.default
spec:
  groups:
  - system:authenticated
  request: $(cat tls.csr | base64 | tr -d '\n')
  usages:
  - digital signature
  - key encipherment
  - server auth
EOF

kubectl certificate approve internal-service-webhook-svc.default

kubectl get csr  internal-service-webhook-svc.default -o jsonpath='{.status.certificate}' \
    | base64 --decode > tls.crt

kubectl create secret tls hook-tls --cert=tls.crt --key=tls.key
