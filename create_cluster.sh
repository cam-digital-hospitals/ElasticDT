echo "CREATING CLUSTER..."
echo
kind create cluster --config Infrastructure/kind.yaml
kubectl config set-context kind-elastic-dt --namespace=default
echo
echo "SETTING UP K8S DASHBOARD..."
echo
. k8s-monitor.sh
echo
echo "APPLYING HELMFILE..."
echo
helmfile sync
echo
echo "DONE..."
echo