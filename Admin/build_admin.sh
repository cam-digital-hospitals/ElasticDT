# Build and deploy an admin pod to the ElasticDT cluster.

docker buildx build . -t elasticdt/admin:0.1.0 && \
kind load docker-image elasticdt/admin:0.1.0 --name elastic-dt && \
kubectl apply -f deployment.yaml && \
kubectl rollout restart deploy/dtadmin

alias kubesh='kubectl exec -it deploy/dtadmin'