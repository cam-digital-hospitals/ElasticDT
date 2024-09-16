# ~/.bashrc: executed by bash(1) for non-login shells.

# Note: PS1 and umask are already set in /etc/profile. You should not
# need this unless you want different defaults for root.
# PS1='${debian_chroot:+($debian_chroot)}\h:\w\$ '
# umask 022

# You may uncomment the following lines if you want `ls' to be colorized:
export LS_OPTIONS='--color=auto'
eval "$(dircolors)"
alias ls='ls $LS_OPTIONS'
alias ll='ls $LS_OPTIONS -l'
alias l='ls $LS_OPTIONS -lA'

# Some more alias to avoid making mistakes:
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Kubernetes
alias kc='kubecolor'
alias pods="kubectl get pod"
alias routes="kubectl get HTTPRoute"

####################################################################

# DATABASE CONNECTIONS

# Configure the MySQL root CLI
alias mysql='mycli -h ds-mysql.elasticdt -u root'

# If you have an InfluxDB token, apply it here:
# influx config set -n elasticdt -t <token>

# Configure the Neo4j root CLI
alias neo4j='cypher-shell -a bolt://ds-neo4j:7687 -u neo4j'

####################################################################

export PS1="\e[0;31m${debian_chroot:+($debian_chroot)}\u@dtadmin:\w\$\e[m "
clear
. /elasticdt/splash.sh