import json
from pathlib import Path

KNOWLEDGE_FILE = Path(__file__).with_name("knowledge_base.json")


def load_knowledge() -> list[dict[str, object]]:
    with KNOWLEDGE_FILE.open(encoding="utf-8") as handle:
        return json.load(handle)


def find_answer(message: str, knowledge: list[dict[str, object]]) -> tuple[str, str]:
    normalized = message.lower().strip()
    best_entry = None
    best_score = 0

    for entry in knowledge:
        keywords = [str(keyword).lower() for keyword in entry["keywords"]]
        score = sum(1 for keyword in keywords if keyword in normalized)
        if score > best_score:
            best_score = score
            best_entry = entry

    if best_entry and best_score > 0:
        return str(best_entry["answer"]), str(best_entry["category"])

    return (
        "I could not find a reliable answer for that request. I have marked it for a human support agent.",
        "escalation",
    )


def main() -> None:
    knowledge = load_knowledge()
    print("Customer Support Assistant")
    print("Type 'exit' to close the session.\n")

    while True:
        message = input("Customer: ").strip()
        if message.lower() in {"exit", "quit"}:
            print("Assistant: Thank you. Goodbye.")
            break
        if not message:
            continue

        answer, category = find_answer(message, knowledge)
        print(f"Assistant: {answer}")
        print(f"Category: {category}\n")


if __name__ == "__main__":
    main()
