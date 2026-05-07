#!/bin/bash

INPUT_APP_TYPE=$1

echo "=================================================="
echo "DYNAMIC APPLICATION TYPE DETECTION"
echo "=================================================="

if [ "$INPUT_APP_TYPE" != "auto-detect" ]; then
  echo "Manual app type selected: $INPUT_APP_TYPE"

  echo "app_type=$INPUT_APP_TYPE" >> $GITHUB_OUTPUT
  echo "language=$INPUT_APP_TYPE" >> $GITHUB_OUTPUT

else
  echo "Auto-detecting application type..."

  if [ -f package.json ]; then
    echo "Node.js application detected"
    echo "app_type=nodejs" >> $GITHUB_OUTPUT
    echo "language=nodejs" >> $GITHUB_OUTPUT

  elif [ -f requirements.txt ]; then
    echo "Python application detected"
    echo "app_type=python" >> $GITHUB_OUTPUT
    echo "language=python" >> $GITHUB_OUTPUT

  elif [ -f pom.xml ]; then
    echo "Java Maven application detected"
    echo "app_type=java" >> $GITHUB_OUTPUT
    echo "language=java" >> $GITHUB_OUTPUT

  elif [ -f build.gradle ]; then
    echo "Java Gradle application detected"
    echo "app_type=java" >> $GITHUB_OUTPUT
    echo "language=java" >> $GITHUB_OUTPUT

  elif [ -f go.mod ]; then
    echo "Go application detected"
    echo "app_type=go" >> $GITHUB_OUTPUT
    echo "language=go" >> $GITHUB_OUTPUT

  elif [ -f Dockerfile ]; then
    echo "Docker application detected"
    echo "app_type=docker" >> $GITHUB_OUTPUT
    echo "language=docker" >> $GITHUB_OUTPUT

  else
    echo "Unknown application type"
    echo "app_type=unknown" >> $GITHUB_OUTPUT
    echo "language=unknown" >> $GITHUB_OUTPUT
  fi
fi

if [ -f Dockerfile ]; then
  echo "has_docker=true" >> $GITHUB_OUTPUT
else
  echo "has_docker=false" >> $GITHUB_OUTPUT
fi

if find . -name "*.tf" | grep -q .; then
  echo "has_terraform=true" >> $GITHUB_OUTPUT
else
  echo "has_terraform=false" >> $GITHUB_OUTPUT
fi

if [ -d k8s ]; then
  echo "has_k8s=true" >> $GITHUB_OUTPUT
else
  echo "has_k8s=false" >> $GITHUB_OUTPUT
fi

echo "=================================================="
echo "Application detection completed"
echo "=================================================="