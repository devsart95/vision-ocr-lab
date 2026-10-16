import argparse
import logging
from pathlib import Path

from ocr_lab.charts import render
from ocr_lab.evaluation import analyze
from ocr_lab.publication import verify
from ocr_lab.runner import replay


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline-first vision extraction lab")
    parser.add_argument("command", choices=["analyze", "verify", "replay"])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--case", default="01")
    parser.add_argument("--model", default="anthropic/claude-haiku-5.5")
    parser.add_argument("--execute-paid", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    if args.command == "replay":
        path = replay(args.root, args.case, args.model, args.execute_paid)
        if path:
            logging.info("Saved %s", path)
        else:
            logging.info("DRY RUN: one call; use --execute-paid to send")
    elif args.command == "verify":
        verify(args.root)
        logging.info("PASS: complete matrix, image hashes, public-content scan, recorded budget")
    else:
        report = analyze(args.root)
        render(report, args.root)
        logging.info("Rebuilt results/summary.json and figures/ without API calls")


if __name__ == "__main__":
    main()
