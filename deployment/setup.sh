openssl req -x509 -newkey rsa:2048 -keyout tls.key -out tls.crt -nodes -subj '/CN=internal-service-webhook-svc.default.svc.cluster.local'
kubectl create secret tls hook-tls --cert=tls.crt --key=tls.key
