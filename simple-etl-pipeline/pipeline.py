from pathlib import Path
import argparse
import logging
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def extract(source: Path) -> pd.DataFrame:
    logging.info("Extracting data from %s", source)
    suffix = source.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(source)
    if suffix == ".json":
        return pd.read_json(source)
    raise ValueError("Only CSV and JSON inputs are supported")


def transform(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Transforming %d rows", len(df))
    required = {"record_id", "customer_name", "email", "amount", "status"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    cleaned = df.copy()
    cleaned["customer_name"] = cleaned["customer_name"].astype(str).str.strip().str.title()
    cleaned["email"] = cleaned["email"].astype(str).str.strip().str.lower()
    cleaned["status"] = cleaned["status"].astype(str).str.strip().str.lower()
    cleaned["amount"] = pd.to_numeric(cleaned["amount"], errors="coerce")

    cleaned = cleaned.drop_duplicates(subset=["record_id"], keep="last")
    cleaned = cleaned.dropna(subset=["record_id", "customer_name", "email", "amount"])
    cleaned = cleaned[cleaned["amount"] >= 0]
    cleaned = cleaned[cleaned["email"].str.contains("@", na=False)]
    cleaned["processed_at"] = pd.Timestamp.utcnow().isoformat()

    return cleaned.sort_values("record_id").reset_index(drop=True)


def load(df: pd.DataFrame, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destination, index=False)
    logging.info("Loaded %d clean rows into %s", len(df), destination)


def run(source: Path, destination: Path) -> None:
    data = extract(source)
    clean_data = transform(data)
    load(clean_data, destination)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a small extract-transform-load pipeline")
    parser.add_argument("source", type=Path)
    parser.add_argument("--destination", type=Path, default=Path("output/clean_customers.csv"))
    args = parser.parse_args()

    try:
        run(args.source, args.destination)
    except (FileNotFoundError, ValueError, pd.errors.ParserError) as exc:
        logging.error("Pipeline failed: %s", exc)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
