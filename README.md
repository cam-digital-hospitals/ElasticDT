# ElasticDT
Scalable, modular, SoA-based DT

## Quickstart

Install Docker, `kubectl`, `kind`, `helm`, and `helmfile`.  Then:

```bash
. util.sh
. create_cluster.sh
helmfile apply
```

To tear down the cluster:
```bash
helmfile destroy
. delete_cluster.sh
```