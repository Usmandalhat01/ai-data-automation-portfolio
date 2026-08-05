# Payroll Data Validator

A small command-line tool for reviewing payroll records before they are imported into another system or used for reporting.

## What it checks

- Missing employee IDs, names, or departments
- Duplicate employee IDs
- Invalid or non-positive salaries
- Employment statuses outside the accepted list

The script produces two files: a validation report and a clean payroll export containing rows that passed all checks.

## Run

```bash
pip install -r requirements.txt
python app.py sample_payroll.csv
```

Use a different output folder when needed:

```bash
python app.py sample_payroll.csv --output-dir reports
```

## Input columns

`employee_id`, `full_name`, `department`, `salary`, `status`

The included sample data is fictional.
