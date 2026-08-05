from pathlib import Path
import argparse
import pandas as pd


def score_match(buyer: pd.Series, seller: pd.Series) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []

    if buyer["category"].strip().lower() == seller["category"].strip().lower():
        score += 40
        reasons.append("same category")
    else:
        return 0, ["category mismatch"]

    if seller["unit_price"] <= buyer["max_unit_price"]:
        score += 25
        reasons.append("within budget")

    if seller["available_quantity"] >= buyer["required_quantity"]:
        score += 20
        reasons.append("quantity available")

    if buyer["location"].strip().lower() == seller["location"].strip().lower():
        score += 10
        reasons.append("same location")

    if str(seller["delivery_available"]).strip().lower() == "yes":
        score += 5
        reasons.append("delivery available")

    return score, reasons


def find_matches(buyers_file: Path, sellers_file: Path, output_file: Path) -> None:
    buyers = pd.read_csv(buyers_file)
    sellers = pd.read_csv(sellers_file)
    matches: list[dict[str, object]] = []

    for _, buyer in buyers.iterrows():
        for _, seller in sellers.iterrows():
            score, reasons = score_match(buyer, seller)
            if score >= 60:
                matches.append({
                    "buyer_id": buyer["buyer_id"],
                    "seller_id": seller["seller_id"],
                    "category": buyer["category"],
                    "match_score": score,
                    "reasons": "; ".join(reasons),
                })

    result = pd.DataFrame(matches)
    if not result.empty:
        result = result.sort_values(["buyer_id", "match_score"], ascending=[True, False])

    output_file.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_file, index=False)
    print(f"Created {len(result)} recommended matches in {output_file}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Match buyers with suitable sellers")
    parser.add_argument("buyers", type=Path)
    parser.add_argument("sellers", type=Path)
    parser.add_argument("--output", type=Path, default=Path("output/matches.csv"))
    args = parser.parse_args()
    find_matches(args.buyers, args.sellers, args.output)


if __name__ == "__main__":
    main()
