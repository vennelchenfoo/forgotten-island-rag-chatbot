"""
evaluate.py — run all four RAG optimization evaluation stages.

Usage:
    python evaluate.py               # runs all stages sequentially
    python evaluate.py --stage 1     # run only the specified stage(s)
    python evaluate.py --stage 1 3   # run stages 1 and 3
"""

import argparse

from evaluation.evaluation_engine import (
    evaluate_baseline,
    evaluate_chunking_strategies,
    evaluate_reranker_strategies,
    evaluate_query_rewriting,
)

STAGES = {
    1: ("Baseline",          evaluate_baseline),
    2: ("Chunking Strategy", evaluate_chunking_strategies),
    3: ("Reranker",          evaluate_reranker_strategies),
    4: ("HyDE Rewriting",    evaluate_query_rewriting),
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run RAG evaluation pipeline.")
    parser.add_argument(
        "--stage",
        nargs="+",
        type=int,
        choices=STAGES.keys(),
        default=list(STAGES.keys()),
        metavar="N",
        help="Stage(s) to run (1=Baseline, 2=Chunking, 3=Reranker, 4=HyDE). "
             "Defaults to all stages.",
    )
    args = parser.parse_args()

    for stage_num in sorted(args.stage):
        label, fn = STAGES[stage_num]
        print(f"\n{'='*60}")
        print(f"  Running Stage {stage_num}: {label}")
        print(f"{'='*60}")
        fn()

    print("\n  All requested evaluation stages complete.")
    print("  Results saved to evaluation/evaluation_results/")


if __name__ == "__main__":
    main()
