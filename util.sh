# Utility scripts for k8s

alias k="kubectl"
alias kls="k config get-contexts"
alias kuse="k config use-context"
ns() {
    kubectl config set-context --current --namespace=$@
}

alias pods="kubectl get pod"

# Use `kubesh -- bash` for a terminal session.
alias kubesh="kubectl exec -it deploy/dtadmin"