#!/bin/bash

echo "Detecting application stack..."

if [ -f "package.json" ]; then
  echo "NODE=true" >> $GITHUB_ENV
  echo "Node.js application detected"
fi

if [ -f "requirements.txt" ]; then
  echo "PYTHON=true" >> $GITHUB_ENV
  echo "Python application detected"
fi

if [ -f "pom.xml" ]; then
  echo "JAVA=true" >> $GITHUB_ENV
  echo "Java application detected"
fi

if [ -f "Dockerfile" ]; then
  echo "DOCKER=true" >> $GITHUB_ENV
  echo "Docker application detected"
fi

if ls *.tf 1> /dev/null 2>&1; then
  echo "TERRAFORM=true" >> $GITHUB_ENV
  echo "Terraform files detected"
fi

if [ -d "k8s" ]; then
  echo "K8S=true" >> $GITHUB_ENV
  echo "Kubernetes manifests detected"
fi