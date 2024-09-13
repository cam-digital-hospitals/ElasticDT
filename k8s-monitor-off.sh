helm uninstall dashboard -n monitoring
kubectl delete ns monitoring
kubectl delete clusterrolebinding dashboard-kubernetes-dashboard
