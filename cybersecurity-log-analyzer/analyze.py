from pathlib import Path
import argparse
import re
import pandas as pd

PATTERNS = [
    (re.compile(r"failed login", re.I), "authentication", "medium"),
    (re.compile(r"multiple failed logins", re.I), "brute-force", "high"),
    (re.compile(r"malware|trojan|ransomware", re.I), "malware", "critical"),
    (re.compile(r"unauthorized access", re.I), "access-control", "high"),
    (re.compile(r"port scan", re.I), "reconnaissance", "medium"),
]


def classify(message: str) -> tuple[str, str]:
    for pattern, category, severity in PATTERNS:
        if pattern.search(message):
            return category, severity
    return "other", "low"


def analyze(input_file: Path, output_file: Path) -> None:
    rows: list[dict[str, str]] = []
    with input_file.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            message = line.strip()
            if not message:
                continue
            category, severity = classify(message)
            rows.append({
                "line": str(line_number),
                "category": category,
                "severity": severity,
                "message": message,
            })

    result = pd.DataFrame(rows)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_file, index=False)

    print(f"Events reviewed: {len(result)}")
    if not result.empty:
        print(result["severity"].value_counts().to_string())
    print(f"Detailed report: {output_file}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify events in a plain-text security log")
    parser.add_argument("input_file", type=Path)
    parser.add_argument("--output", type=Path, default=Path("output/security_findings.csv"))
    args = parser.parse_args()
    analyze(args.input_file, args.output)


if __name__ == "__main__":
    main()
