from pathlib import Path
import argparse
import pandas as pd

REQUIRED_COLUMNS = {"employee_id", "full_name", "department", "salary", "status"}
VALID_STATUSES = {"active", "inactive", "suspended"}


def validate_payroll(input_file: Path, output_dir: Path) -> None:
    df = pd.read_csv(input_file)
    missing_columns = REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing_columns))}")

    issues: list[dict[str, object]] = []

    for index, row in df.iterrows():
        row_number = index + 2
        employee_id = str(row.get("employee_id", "")).strip()
        full_name = str(row.get("full_name", "")).strip()
        department = str(row.get("department", "")).strip()
        status = str(row.get("status", "")).strip().lower()
        salary = pd.to_numeric(row.get("salary"), errors="coerce")

        if not employee_id:
            issues.append({"row": row_number, "employee_id": employee_id, "issue": "Missing employee ID"})
        if not full_name:
            issues.append({"row": row_number, "employee_id": employee_id, "issue": "Missing employee name"})
        if not department:
            issues.append({"row": row_number, "employee_id": employee_id, "issue": "Missing department"})
        if pd.isna(salary) or salary <= 0:
            issues.append({"row": row_number, "employee_id": employee_id, "issue": "Invalid salary"})
        if status not in VALID_STATUSES:
            issues.append({"row": row_number, "employee_id": employee_id, "issue": "Invalid employment status"})

    duplicates = df[df["employee_id"].astype(str).duplicated(keep=False)]
    for index, row in duplicates.iterrows():
        issues.append({
            "row": index + 2,
            "employee_id": row["employee_id"],
            "issue": "Duplicate employee ID",
        })

    output_dir.mkdir(parents=True, exist_ok=True)
    issue_df = pd.DataFrame(issues, columns=["row", "employee_id", "issue"])
    issue_df.to_csv(output_dir / "validation_report.csv", index=False)

    invalid_rows = set(issue_df["row"].tolist()) if not issue_df.empty else set()
    clean_df = df[[index + 2 not in invalid_rows for index in range(len(df))]].copy()
    clean_df.to_csv(output_dir / "clean_payroll.csv", index=False)

    print(f"Rows reviewed: {len(df)}")
    print(f"Issues found: {len(issue_df)}")
    print(f"Clean rows exported: {len(clean_df)}")
    print(f"Reports saved to: {output_dir.resolve()}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a payroll CSV file")
    parser.add_argument("input_file", type=Path, help="Path to the payroll CSV")
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    args = parser.parse_args()

    try:
        validate_payroll(args.input_file, args.output_dir)
    except (FileNotFoundError, ValueError, pd.errors.ParserError) as exc:
        raise SystemExit(f"Validation failed: {exc}") from exc


if __name__ == "__main__":
    main()
