import os
import argparse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

parser = argparse.ArgumentParser()

parser.add_argument("--to", required=True)
parser.add_argument("--from-email", required=True)
parser.add_argument("--app-name", required=True)
parser.add_argument("--critical", required=True)
parser.add_argument("--high", required=True)
parser.add_argument("--medium", required=True)
parser.add_argument("--pipeline-url", required=True)
parser.add_argument("--reports-dir", required=True)

args = parser.parse_args()

to_email = args.to
from_email = args.from_email
app_name = args.app_name

critical = args.critical
high = args.high
medium = args.medium

pipeline_url = args.pipeline_url

html_content = f"""
<h2>Dynamic DevSecOps Security Alert</h2>

<p><strong>Application:</strong> {app_name}</p>

<h3>Vulnerability Summary</h3>

<table border="1" cellpadding="8" cellspacing="0">
<tr>
<th>Severity</th>
<th>Count</th>
</tr>

<tr>
<td>Critical</td>
<td>{critical}</td>
</tr>

<tr>
<td>High</td>
<td>{high}</td>
</tr>

<tr>
<td>Medium</td>
<td>{medium}</td>
</tr>

</table>

<br>

<p>
Deployment has been paused because vulnerabilities exceeded policy threshold.
</p>

<p>
Manual approval is required before deployment can continue.
</p>

<p>
<a href="{pipeline_url}">
Open GitHub Actions Pipeline
</a>
</p>

<br>

<p>
Dynamic DevSecOps Platform
</p>
"""

message = Mail(
    from_email=from_email,
    to_emails=to_email,
    subject=f"[SECURITY ALERT] {app_name} vulnerabilities detected",
    html_content=html_content
)

try:

    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))

    response = sg.send(message)

    print("==================================================")
    print("EMAIL ALERT SENT SUCCESSFULLY")
    print("==================================================")

    print(f"Status Code : {response.status_code}")

except Exception as e:

    print("==================================================")
    print("EMAIL SENDING FAILED")
    print("==================================================")

    print(str(e))