# Simple ETL Pipeline

A small extract-transform-load workflow that reads CSV or JSON data, standardizes names and emails, validates numeric fields, removes duplicate records, drops invalid rows, and writes a clean CSV output.

## Run

```bash
pip install pandas
python pipeline.py sample_customers.csv
```

A custom output path can be supplied with:

```bash
python pipeline.py sample_customers.csv --destination reports/clean_customers.csv
```

The script includes basic logging and clear failure messages so the flow is easy to troubleshoot.
