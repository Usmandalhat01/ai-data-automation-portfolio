from pathlib import Path
from datetime import datetime, timezone
import argparse
import pandas as pd


def days_old(value: str) -> int | None:
    if not value or pd.isna(value):
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - parsed).days
    except ValueError:
        return None


def audit_users(input_file: Path, output_file: Path) -> None:
    users = pd.read_csv(input_file)
    findings: list[dict[str, object]] = []

    for _, user in users.iterrows():
        username = user["user_name"]
        if str(user.get("mfa_enabled", "")).lower() != "true":
            findings.append({"user_name": username, "severity": "high", "finding": "MFA is not enabled"})

        key_age = days_old(user.get("access_key_created"))
        if key_age is not None and key_age > 90:
            findings.append({"user_name": username, "severity": "medium", "finding": f"Access key is {key_age} days old"})

        last_used_age = days_old(user.get("password_last_used"))
        if last_used_age is not None and last_used_age > 90:
            findings.append({"user_name": username, "severity": "low", "finding": f"Console password unused for {last_used_age} days"})

        policies = str(user.get("attached_policies", ""))
        if "AdministratorAccess" in policies:
            findings.append({"user_name": username, "severity": "high", "finding": "AdministratorAccess policy attached"})

    output_file.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(findings, columns=["user_name", "severity", "finding"]).to_csv(output_file, index=False)
    print(f"Audit completed. {len(findings)} findings written to {output_file}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Review an exported AWS IAM user report")
    parser.add_argument("input_file", type=Path)
    parser.add_argument("--output", type=Path, default=Path("output/iam_findings.csv"))
    args = parser.parse_args()
    audit_users(args.input_file, args.output)


if __name__ == "__main__":
    main()
