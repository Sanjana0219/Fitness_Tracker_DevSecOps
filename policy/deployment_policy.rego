package devsecops.policy

deny[msg] {
    input.critical_count > 0
    msg := "Critical vulnerabilities detected"
}

deny[msg] {
    input.high_count > 0
    msg := "High vulnerabilities detected"
}

deny[msg] {
    input.secrets_count > 0
    msg := "Secrets detected in repository"
}