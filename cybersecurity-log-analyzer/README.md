# Cybersecurity Log Analyzer

A plain-text log review tool that classifies common security events such as failed logins, brute-force attempts, malware detections, unauthorized access, and port scans.

## Run

```bash
pip install pandas
python analyze.py sample.log
```

The script creates `output/security_findings.csv` and prints a severity summary in the terminal.

This is a learning and reporting tool, not a replacement for a SIEM or professional incident-response platform.
