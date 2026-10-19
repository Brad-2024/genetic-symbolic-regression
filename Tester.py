import argparse
import csv
import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt


def count_tree_nodes(log_path):
    with Path(log_path).open(encoding="utf-8") as log_file:
        for line_number, line in enumerate(log_file, start=1):
            line = line.strip()
            if not line:
                continue

            match = re.match(r"^(\d+)\s+(.*)$", line)
            if match is None:
                raise ValueError(f"Line {line_number} does not start with an index and tree.")

            index, tree_and_fitness = match.groups()
            node_count = tree_and_fitness.count("(")
            yield int(index), node_count


def main():
    parser = argparse.ArgumentParser(
        description="Plot tree node counts from a genetic algorithm output log."
    )
    parser.add_argument("log_file", help="Path to the genetic algorithm output log.")
    parser.add_argument(
        "--save",
        metavar="PATH",
        help="Save the plot to PATH instead of opening the interactive plot window.",
    )
    args = parser.parse_args()

    entries = list(count_tree_nodes(args.log_file))
    if not entries:
        raise ValueError(f"No indexed tree entries found in {args.log_file!r}.")

    indices, node_counts = zip(*entries)
    plt.plot(indices, node_counts, "b.-")
    plt.xlabel("Entry")
    plt.ylabel("Number of nodes")
    plt.title(f"Tree size by entry: {Path(args.log_file).name}")
    plt.grid(True)
    plt.tight_layout()

    if args.save:
        plt.savefig(args.save)
        print(f"Plot saved to {args.save}")
    else:
        plt.show()


if __name__ == "__main__":
    main()