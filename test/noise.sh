# create/delete service to see how things are working.
while true; do
  echo `date`
  kubectl create svc nodeport drf-test --tcp 80:80
  kubectl get svc drf-test -o yaml
  kubectl delete svc drf-test
done
