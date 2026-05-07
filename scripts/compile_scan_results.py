import json
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--reports-dir", required=True)
parser.add_argument("--output", required=True)

args = parser.parse_args()

reports_dir = args.reports_dir
output_file = args.output

summary = {
    "critical_count": 0,
    "high_count": 0,
    "medium_count": 0,
    "low_count": 0,
    "secrets_count": 0
}

def load_json(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

# ---------------------------------------------------
# GitLeaks Secrets
# ---------------------------------------------------

gitleaks_file = os.path.join(reports_dir, "gitleaks-report.json")

if os.path.exists(gitleaks_file):
    data = load_json(gitleaks_file)

    if isinstance(data, list):
        summary["secrets_count"] = len(data)

# ---------------------------------------------------
# Trivy Container Scan
# ---------------------------------------------------

trivy_file = os.path.join(reports_dir, "trivy-report.json")

if os.path.exists(trivy_file):
    data = load_json(trivy_file)

    if data and "Results" in data:

        for result in data["Results"]:

            vulnerabilities = result.get("Vulnerabilities", [])

            for vuln in vulnerabilities:

                severity = vuln.get("Severity", "").upper()

                if severity == "CRITICAL":
                    summary["critical_count"] += 1

                elif severity == "HIGH":
                    summary["high_count"] += 1

                elif severity == "MEDIUM":
                    summary["medium_count"] += 1

                elif severity == "LOW":
                    summary["low_count"] += 1

# ---------------------------------------------------
# npm audit
# ---------------------------------------------------

npm_file = os.path.join(reports_dir, "npm-audit.json")

if os.path.exists(npm_file):

    try:
        with open(npm_file, "r", encoding="utf-8") as f:
            npm_data = json.load(f)

        vulnerabilities = npm_data.get("vulnerabilities", {})

        for _, vuln in vulnerabilities.items():

            severity = vuln.get("severity", "").upper()

            if severity == "CRITICAL":
                summary["critical_count"] += 1

            elif severity == "HIGH":
                summary["high_count"] += 1

            elif severity == "MEDIUM":
                summary["medium_count"] += 1

            elif severity == "LOW":
                summary["low_count"] += 1

    except:
        pass

# ---------------------------------------------------
# Checkov IaC Scan
# ---------------------------------------------------

checkov_file = os.path.join(reports_dir, "checkov-report.json")

if os.path.exists(checkov_file):

    try:
        with open(checkov_file, "r", encoding="utf-8") as f:
            content = f.read()

        if content.strip():

            try:
                checkov_data = json.loads(content)

                if isinstance(checkov_data, dict):

                    results = checkov_data.get("results", {})

                    failed_checks = results.get("failed_checks", [])

                    for check in failed_checks:

                        severity = str(
                            check.get("severity", "MEDIUM")
                        ).upper()

                        if severity == "CRITICAL":
                            summary["critical_count"] += 1

                        elif severity == "HIGH":
                            summary["high_count"] += 1

                        elif severity == "MEDIUM":
                            summary["medium_count"] += 1

                        else:
                            summary["low_count"] += 1

            except:
                pass

    except:
        pass

# ---------------------------------------------------
# Save Final Summary
# ---------------------------------------------------

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=4)

print("==================================================")
print("FINAL SECURITY SUMMARY")
print("==================================================")

for k, v in summary.items():
    print(f"{k}: {v}")

print("==================================================")
print(f"Summary saved to: {output_file}")
print("==================================================")