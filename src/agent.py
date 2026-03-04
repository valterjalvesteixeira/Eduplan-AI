from pathlib import Path

from src.logger import JSONLLogger
from src.planner import mock_plan
from src.tools import write_file
from src.validator import validate_total_duration


class EduPlanAgent:
    """
    Orchestrates the workflow:
    1) Generate a structured plan (EduPlan)
    2) Validate business rules (e.g., total duration)
    3) Save plan.json
    4) Render final.md
    5) Log events to run_log.jsonl
    """

    def __init__(self, run_dir: Path, logger: JSONLLogger):
        self.run_dir = run_dir
        self.logger = logger

    def run(self, goal: str, target_audience: str, duration_minutes: int) -> None:
        # Planning
        self.logger.log(
            phase="planning",
            status="started",
            details={"goal": goal, "audience": target_audience, "duration": duration_minutes},
        )

        plan = mock_plan(goal=goal, target_audience=target_audience, duration_minutes=duration_minutes)

        self.logger.log(
            phase="planning",
            status="success",
            details={"message": "Plan generated and schema-validated (Pydantic)."},
        )

        # Validation (business rule)
        try:
            validate_total_duration(plan)
            self.logger.log("validation", "success", {"rule": "total_duration"})
        except ValueError as e:
            self.logger.log("validation", "failed", {"rule": "total_duration", "error": str(e)})
            raise

        # Save plan.json
        plan_path = self.run_dir / "plan.json"
        write_file(plan_path, plan.model_dump_json(indent=2))
        self.logger.log("io", "success", {"action": "write_file", "path": str(plan_path)})

        # Delivery (final.md)
        final_md = self._render_markdown(plan.model_dump())
        final_path = self.run_dir / "final.md"
        write_file(final_path, final_md)
        self.logger.log("delivery", "success", {"final_path": str(final_path)})

    def _render_markdown(self, plan_dict: dict) -> str:
        meta = plan_dict["meta"]

        lines = []
        lines.append("# EduPlan AI — Educational Plan\n")
        lines.append(f"Theme: {meta['theme']}")
        lines.append(f"Target audience: {meta['target_audience']}")
        lines.append(f"Total duration: {meta['duration_total_minutes']} minutes\n")

        lines.append("## Learning Objectives")
        for obj in plan_dict["learning_objectives"]:
            lines.append(f"- {obj}")
        lines.append("")

        lines.append("## Activities")
        for a in plan_dict["activities"]:
            lines.append(f"### {a['id']} — {a['title']}")
            lines.append(f"- Duration: {a['duration_minutes']} minutes")
            lines.append(f"- Description: {a['description']}")
            if a["materials"]:
                lines.append(f"- Materials: {', '.join(a['materials'])}")
            if a["skills_targeted"]:
                lines.append(f"- Skills targeted: {', '.join(a['skills_targeted'])}")
            lines.append(f"- Assessment: {a['assessment_method']}\n")

        lines.append("## Risks & Mitigations")
        for r in plan_dict.get("risk_analysis", []):
            lines.append(f"- Risk: {r['risk']} | Mitigation: {r['mitigation']}")
        lines.append("")

        if plan_dict.get("commercial_summary"):
            lines.append("## Commercial Summary")
            lines.append(plan_dict["commercial_summary"])
            lines.append("")

        return "\n".join(lines)