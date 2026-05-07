Write-Host "Detecting application stack..."

$ProjectRoot = Split-Path -Parent $PSScriptRoot

if (Test-Path "$ProjectRoot\package.json") {
    Write-Host "Node.js application detected"
}

if (Test-Path "$ProjectRoot\requirements.txt") {
    Write-Host "Python application detected"
}

if (Test-Path "$ProjectRoot\pom.xml") {
    Write-Host "Java application detected"
}

if (Test-Path "$ProjectRoot\Dockerfile") {
    Write-Host "Docker application detected"
}

if (Get-ChildItem "$ProjectRoot" -Filter "*.tf" -ErrorAction SilentlyContinue) {
    Write-Host "Terraform detected"
}

if (Test-Path "$ProjectRoot\k8s") {
    Write-Host "Kubernetes manifests detected"
}