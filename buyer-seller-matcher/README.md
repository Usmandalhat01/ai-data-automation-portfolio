# Buyer-Seller Matcher

This project applies simple business rules to recommend suitable sellers for each buyer. It scores matches using product category, budget, quantity, location, and delivery availability.

## Run

```bash
pip install pandas
python app.py sample_buyers.csv sample_sellers.csv
```

Matches scoring 60 or more are exported to `output/matches.csv` and sorted from strongest to weakest for each buyer.

The data included here is fictional and only demonstrates the matching logic.
