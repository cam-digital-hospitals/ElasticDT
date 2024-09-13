echo 'Installing Helm chart for Kubernetes dashboard...'
echo

helm install dashboard kubernetes-dashboard/kubernetes-dashboard \
-n monitoring --create-namespace \
--set metrics-server.enabled=true --wait --timeout 60s

kubectl -n monitoring create \
clusterrolebinding dashboard-kubernetes-dashboard \
--clusterrole=cluster-admin \
--serviceaccount=monitoring:default

kubectl -n monitoring create token default \
--duration 8760h > $HOME/kind-dashboard-token

echo "Kubernetes dashboard installed in the current \"$(kubectl config current-context)\" context."
echo
echo "Use the following bearer token to login:"
cat $HOME/kind-dashboard-token
echo
echo

nohup kubectl -n monitoring port-forward svc/dashboard-kong-proxy 8443:443 &>/dev/null &
