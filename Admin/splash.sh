 printf '\033[31m'
 cat << EOF
 _______        _______ _______ _______ _____ _______   ______  _______
 |______ |      |_____| |______    |      |   |         |     \    |   
 |______ |_____ |     | ______|    |    __|__ |_____    |_____/    |   
------------------------------------------------------------------------
EOF
printf '\033[m'

cat << 'EOF'
ElasticDT Demonstratior -- Admin Pod
(c) 2024 Institute for Manufacturing, Cambridge University
Maintainers: Yin-Chi Chan <ycc39>; Anandarup Mukherjee <am2910>

Available programs:
 - kubecolor: kubectl with colour. Use `kc` as an alias.
 - mycli: MySQL/MariaDB client with auto-completion. Use the `mysql`
   alias to connect to the ds-mysql service on this cluster.
 - influx: CLI for InfluxDB
 - neo4j: CLI for Neo4j, aliased on this machine to connect to the
   ds-neo4j service on this cluster.

Use `alias` to view the complete list of configured bash aliases.
EOF
