# Utility scripts for k8s

alias k="kubectl"
ns() {
    kubectl config set-context --current --namespace=$@
}
alias pods="kubectl get pod"