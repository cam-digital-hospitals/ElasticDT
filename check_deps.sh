#!/bin/bash

# Function to print text in red
print_red() {
    echo -e "\e[31m$1\e[0m"
}

if command -v docker &> /dev/null
then
    echo "Docker binary path: $(command -v docker)"   
    echo "$(docker --version)"
else
    print_red "Docker not installed"
fi
echo

if command -v kubectl &> /dev/null
then
    echo "kubectl binary path: $(command -v kubectl)"   
    echo "$(kubectl version --client)"
else
    print_red "kubectl not installed"
fi
echo

if command -v kind &> /dev/null
then
    echo "kind binary path: $(command -v kind)"   
    echo "$(kind version)"
else
    print_red "kind not installed"
fi
echo

if command -v helm &> /dev/null
then
    echo "Helm binary path: $(command -v helm)"   
    echo "$(helm version)"
else
    print_red "Helm not installed"
fi
echo

if command -v helmfile &> /dev/null
then
    echo "helmfile binary path: $(command -v helmfile)"   
    echo "$(helmfile --version)"
else
    print_red "helmfile not installed"
fi
echo