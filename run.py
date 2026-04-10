import argparse
from datetime import datetime
from pathlib import Path

from src.agent import EduPlanAgent
from src.logger import JSONLLogger


def create_run_dir(base_dir: Path) -> Path:
    """
    Create a unique run folder under /runs using a timestamp.
    Example: runs/2026-03-04_121530
    """
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    run_dir = base_dir / ts
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="EduPlan AI — Structured Educational Planning Agent")
    parser.add_argument("--goal", required=True, help="Theme / goal of the educational plan")
    parser.add_argument("--audience", required=True, help="Target audience (e.g. 10-12 years old)")
    parser.add_argument("--duration", type=int, default=60, help="Total duration in minutes")
    args = parser.parse_args()

    run_dir = create_run_dir(Path("runs"))
    logger = JSONLLogger(run_dir / "run_log.jsonl")

    agent = EduPlanAgent(run_dir=run_dir, logger=logger)
    agent.run(goal=args.goal, target_audience=args.audience, duration_minutes=args.duration)

    print(f"Done. Outputs saved in: {run_dir}")


if __name__ == "__main__":
    main()