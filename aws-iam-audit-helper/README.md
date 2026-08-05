# AWS IAM Audit Helper

A simple review tool for IAM user exports. It flags missing MFA, old access keys, long-unused console passwords, and accounts with the `AdministratorAccess` policy.

## Run

```bash
pip install pandas
python audit.py sample_iam_users.csv
```

The output is written to `output/iam_findings.csv`.

This project uses sample export data rather than connecting directly to an AWS account, which makes it safe to test locally.
