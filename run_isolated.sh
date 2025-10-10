#!/bin/bash

export PYTHONIOENCODING="utf-8"
export KUBECONFIG="$1"
export MODEL="$2"

echo "Script started with arguments:"
echo "KUBECONFIG: $KUBECONFIG"
echo "MODEL: $MODEL"

RANDOM_ID=$((RANDOM))
kind delete cluster --kubeconfig $KUBECONFIG --name isolated-$RANDOM_ID
kind create cluster --config kind/kind-config-x86.yaml --kubeconfig $KUBECONFIG --name isolated-$RANDOM_ID

if [ "$#" -eq 4 ]; then
    echo "Running isolated React client with resume ID $3 and start index $4..."
    tmux new "KUBECONFIG=$KUBECONFIG MODEL=$MODEL ./.venv/bin/python3 clients/isolated_react.py --resume-id $3 --start-idx $4"
else
    echo "Running isolated React client..."
    tmux new "KUBECONFIG=$KUBECONFIG MODEL=$MODEL ./.venv/bin/python3 clients/isolated_react.py"
fi
