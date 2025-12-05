"""Generate a processed CSV from the raw MachineLearningRating_v3 dataset.

This script uses the project's DataLoader to read the raw pipe-separated
text file and writes a CSV version to data/processed/.
"""

from __future__ import annotations

from pathlib import Path
import sys

# Ensure project root (parent of scripts/) is on sys.path so we can import src
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import DataLoader


def main() -> None:
    loader = DataLoader.from_config()
    df = loader.load_machine_learning_rating()

    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "MachineLearningRating_v3.csv"

    df.to_csv(output_path, index=False)
    print(f"Wrote processed CSV to {output_path}")


if __name__ == "__main__":
    main()
