# src/llm_planner.py

from __future__ import annotations

import json
from typing import Optional, Literal, List

from openai import OpenAI
from pydantic import ValidationError

from src.schemas import EduPlan
from src.prompts import SYSTEM_PROMPT


EducationLevel = Literal["Pre-school", "Primary School", "Lower Secondary", "Upper Secondary"]


class LLMPlannerError(RuntimeError):
    """Generic error raised by the LLM planner."""


class LLMPlannerValidationError(LLMPlannerError):
    """Raised when the LLM output cannot be validated against the EduPlan schema."""


def _normalize_level(level: str) -> EducationLevel:
    """Normalize common inputs to the exact allowed labels."""
    l = level.strip().lower()

    mapping = {
        "preschool": "Pre-school",
        "pre-school": "Pre-school",
        "pre school": "Pre-school",
        "kindergarten": "Pre-school",
        "infant": "Pre-school",

        "primary": "Primary School",
        "primary school": "Primary School",
        "elementary": "Primary School",
        "elementary school": "Primary School",

        "lower secondary": "Lower Secondary",
        "middle school": "Lower Secondary",
        "basic education": "Lower Secondary",
        "2nd cycle": "Lower Secondary",
        "3rd cycle": "Lower Secondary",

        "upper secondary": "Upper Secondary",
        "secondary": "Upper Secondary",
        "high school": "Upper Secondary",
        "grade 10": "Upper Secondary",
        "grade 11": "Upper Secondary",
        "grade 12": "Upper Secondary",
    }

    if l in mapping:
        return mapping[l]  # type: ignore[return-value]

    # Accept exact labels too
    exact = {
        "pre-school": "Pre-school",
        "primary school": "Primary School",
        "lower secondary": "Lower Secondary",
        "upper secondary": "Upper Secondary",
    }
    if l in exact:
        return exact[l]  # type: ignore[return-value]

    raise ValueError(
        f"Invalid education_level: {level}. "
        "Use one of: Pre-school, Primary School, Lower Secondary, Upper Secondary."
    )


def _build_user_prompt(
    goal: str,
    target_audience: str,
    duration_minutes: int,
    education_level: Optional[EducationLevel] = None,
    constraints: Optional[str] = None,
) -> str:
    extra = f"\nAdditional constraints:\n{constraints}\n" if constraints else ""

    if education_level:
        level_instruction = f"""
Generate activities ONLY for this education level:
{education_level}

Still return JSON in the schema format.
For other levels, return empty activities arrays.
"""
    else:
        level_instruction = """
Generate activities for ALL education levels:
Pre-school, Primary School, Lower Secondary, Upper Secondary
"""

    # This forces the model into the exact outer structure the schema expects.
    schema_hint = """
Return JSON with EXACTLY this top-level structure:
{
  "meta": {"theme": "...", "total_duration_minutes": 60, "notes": "..."},
  "learning_objectives": ["...", "...", "..."],
  "levels": [
    {"level": "Pre-school", "activities": [ ... ]},
    {"level": "Primary School", "activities": [ ... ]},
    {"level": "Lower Secondary", "activities": [ ... ]},
    {"level": "Upper Secondary", "activities": [ ... ]}
  ],
  "risk_analysis": [{"risk": "...", "mitigation": "..."}]
}

Each activity must include:
title, recommended_age_group, learning_goals (list),
ai_tool_or_concept, estimated_duration_minutes,
materials_and_technology (list),
steps (list),
engagement_rationale,
skills_developed (list),
multicultural_adaptations (list),
extension_activity
"""

    return f"""
Create an AI-supported classroom activity plan.

Theme / focus: {goal}
Target audience notes: {target_audience}
Total duration: {duration_minutes} minutes
{extra}

{level_instruction}

Rules:
- Teacher-friendly, minimal preparation
- Active learning; students interact with AI
- Encourage discussion and critical thinking about AI outputs
- Return ONLY JSON (no markdown, no commentary)

{schema_hint}
""".strip()


def _ensure_all_levels_present(plan_dict: dict, requested_level: Optional[EducationLevel]) -> dict:
    """
    Ensure the plan has all 4 levels in the expected order.
    If requested_level is provided, keep activities only for that level, empty for others.
    """
    expected_levels: List[EducationLevel] = [
        "Pre-school",
        "Primary School",
        "Lower Secondary",
        "Upper Secondary",
    ]

    levels = plan_dict.get("levels", [])
    if not isinstance(levels, list):
        levels = []

    # Index current levels by name
    by_level = {}
    for item in levels:
        if isinstance(item, dict) and "level" in item:
            by_level[item["level"]] = item

    new_levels = []
    for lvl in expected_levels:
        item = by_level.get(lvl, {"level": lvl, "activities": []})
        if requested_level and lvl != requested_level:
            item["activities"] = []
        new_levels.append(item)

    plan_dict["levels"] = new_levels

    # Put a helpful note
    meta = plan_dict.get("meta") or {}
    if not isinstance(meta, dict):
        meta = {}
    notes = meta.get("notes") or ""
    if requested_level:
        meta["notes"] = (notes + " " if notes else "") + f"Requested level: {requested_level}."
    plan_dict["meta"] = meta

    return plan_dict


def generate_plan_llm(
    goal: str,
    target_audience: str,
    duration_minutes: int,
    education_level: Optional[str] = None,
    model: str = "gpt-4o-mini",
    temperature: float = 0.4,
    constraints: Optional[str] = None,
) -> EduPlan:
    """
    Generate an educational plan using an LLM and validate it against the EduPlan schema.

    If education_level is provided, the model is instructed to generate only that level and
    the code will ensure the other levels are present but empty to keep schema validity.
    """
    if not isinstance(duration_minutes, int) or duration_minutes <= 0:
        raise ValueError("duration_minutes must be a positive integer")

    requested_level: Optional[EducationLevel] = None
    if education_level:
        requested_level = _normalize_level(education_level)

    client = OpenAI()

    user_prompt = _build_user_prompt(
        goal=goal,
        target_audience=target_audience,
        duration_minutes=duration_minutes,
        education_level=requested_level,
        constraints=constraints,
    )

    try:
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT.strip()},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )
    except Exception as e:
        raise LLMPlannerError(f"OpenAI request failed: {e}") from e

    content = (response.choices[0].message.content or "").strip()

    # Parse JSON
    try:
        plan_dict = json.loads(content)
    except json.JSONDecodeError as e:
        raise LLMPlannerValidationError(
            "Model did not return valid JSON. Tighten the prompt or change model."
        ) from e

    # Ensure structure matches schema expectations
    plan_dict = _ensure_all_levels_present(plan_dict, requested_level)

    # Validate
    try:
        return EduPlan.model_validate(plan_dict)
    except ValidationError as e:
        raise LLMPlannerValidationError(
            "Model JSON does not match EduPlan schema. "
            "Update schema or tighten prompt (fields, types, required keys)."
        ) from e